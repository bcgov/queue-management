import fs from 'node:fs/promises'
import http from 'node:http'
import path from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const isProd = process.env.NODE_ENV === 'production'
const port = Number(process.env.PORT || 5173)

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

server.listen(port, () => {
  // Keep startup logging concise for local dev and container logs.
  console.log(`SSR server running on http://localhost:${port}`)
})