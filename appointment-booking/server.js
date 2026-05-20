import fs from 'node:fs/promises'
import http from 'node:http'
import path from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const isProd = process.env.NODE_ENV === 'production'
const preferredPort = Number(process.env.PORT || 5173)
const fallbackPort = Number(process.env.FALLBACK_PORT || preferredPort + 1)

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