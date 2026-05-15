import fs from 'node:fs/promises'
import http from 'node:http'
import path from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const isProd = process.env.NODE_ENV === 'production'
const preferredPort = Number(process.env.PORT || 5173)
const fallbackPort = Number(process.env.FALLBACK_PORT || preferredPort + 1)
const apiProxyTarget = (process.env.API_PROXY_TARGET || 'http://localhost:5000').replace(/\/$/, '')

const mimeTypes = {
  '.css': 'text/css; charset=utf-8',
  '.ico': 'image/x-icon',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
}

let vite
if (!isProd) {
  const { createServer } = await import('vite')
  vite = await createServer({
    appType: 'custom',
    root: __dirname,
    server: { middlewareMode: true },
  })
}

const prodTemplate = isProd
  ? await fs.readFile(path.resolve(__dirname, 'dist/client/index.html'), 'utf-8')
  : ''

const distClientDir = path.resolve(__dirname, 'dist/client')

function send(res, statusCode, body, headers = {}) {
  res.writeHead(statusCode, headers)
  res.end(body)
}

function getRequestBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = []
    req.on('data', (chunk) => chunks.push(chunk))
    req.on('end', () => {
      if (!chunks.length) {
        resolve(undefined)
        return
      }

      resolve(Buffer.concat(chunks))
    })
    req.on('error', reject)
  })
}

async function tryProxyApiRequest(req, res, urlPath) {
  if (!urlPath.startsWith('/api/v1')) {
    return false
  }

  const targetUrl = `${apiProxyTarget}${urlPath}`
  const requestBody = await getRequestBody(req)

  try {
    const proxyResponse = await fetch(targetUrl, {
      method: req.method,
      headers: {
        ...(req.headers || {}),
        host: undefined,
      },
      body: requestBody,
    })

    const responseBuffer = Buffer.from(await proxyResponse.arrayBuffer())
    send(res, proxyResponse.status, responseBuffer, {
      'Content-Type': proxyResponse.headers.get('content-type') || 'application/json; charset=utf-8',
    })
    return true
  } catch {
    send(res, 502, JSON.stringify({ message: 'Unable to reach booking API' }), {
      'Content-Type': 'application/json; charset=utf-8',
    })
    return true
  }
}

function getRuntimeConfig() {
  return {
    apiBaseUrl: process.env.API_BASE_URL || process.env.VITE_API_BASE_URL || '/api/v1',
    requestTimeoutMs: Number(process.env.REQUEST_TIMEOUT_MS || 10000),
  }
}

async function renderPage(url, res) {
  let template
  let render

  if (!isProd) {
    template = await fs.readFile(path.resolve(__dirname, 'index.html'), 'utf-8')
    template = await vite.transformIndexHtml(url, template)
    render = (await vite.ssrLoadModule('/src/entry-server.tsx')).render
  } else {
    template = prodTemplate
    render = (await import(pathToFileURL(path.resolve(__dirname, 'dist/server/entry-server.js')).href)).render
  }

  const { appHtml } = await render(url)
  const html = template.replace('<!--ssr-outlet-->', appHtml)

  send(res, 200, html, { 'Content-Type': 'text/html; charset=utf-8' })
}

async function tryServeStatic(urlPath, res) {
  if (!isProd) {
    return false
  }

  const normalizedPath = decodeURIComponent(urlPath.split('?')[0])
  const requestedFile = normalizedPath === '/' ? '/index.html' : normalizedPath
  const absolutePath = path.resolve(distClientDir, `.${requestedFile}`)

  if (!absolutePath.startsWith(distClientDir)) {
    send(res, 403, 'Forbidden')
    return true
  }

  try {
    const file = await fs.readFile(absolutePath)
    const extension = path.extname(absolutePath)
    const contentType = mimeTypes[extension] || 'application/octet-stream'
    send(res, 200, file, { 'Content-Type': contentType })
    return true
  } catch {
    return false
  }
}

const server = http.createServer(async (req, res) => {
  const url = req.url || '/'

  try {
    const proxied = await tryProxyApiRequest(req, res, url)
    if (proxied) {
      return
    }
  } catch {
    send(res, 500, 'Internal Server Error')
    return
  }

  if (url.startsWith('/config/runtime-config.json')) {
    send(res, 200, JSON.stringify(getRuntimeConfig()), {
      'Cache-Control': 'no-store',
      'Content-Type': 'application/json; charset=utf-8',
    })
    return
  }

  if (!isProd && vite) {
    return vite.middlewares(req, res, async () => {
      try {
        await renderPage(url, res)
      } catch (error) {
        vite.ssrFixStacktrace(error)
        send(res, 500, 'Internal Server Error')
      }
    })
  }

  try {
    const served = await tryServeStatic(url, res)
    if (served) {
      return
    }

    await renderPage(url, res)
  } catch {
    send(res, 500, 'Internal Server Error')
  }
})

let isRetryingWithFallbackPort = false

function startServer(onPort) {
  server.listen(onPort, () => {
    // Keep startup logging concise for local dev and container logs.
    console.log(`SSR server running on http://localhost:${onPort}`)
  })
}

server.on('error', (error) => {
  if (
    error &&
    error.code === 'EADDRINUSE' &&
    !isRetryingWithFallbackPort &&
    preferredPort !== fallbackPort
  ) {
    isRetryingWithFallbackPort = true
    console.warn(`Port ${preferredPort} is already in use. Falling back to ${fallbackPort}.`)
    startServer(fallbackPort)
    return
  }

  throw error
})

startServer(preferredPort)