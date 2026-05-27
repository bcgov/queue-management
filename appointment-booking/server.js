import fs from 'node:fs/promises'
import { createServer } from 'node:http'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const port = Number(process.env.PORT || 5173)
const distDir = path.resolve(__dirname, 'dist')

const mimeTypes = {
  '.css': 'text/css',
  '.html': 'text/html; charset=utf-8',
  '.ico': 'image/x-icon',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
}

const runtimeConfig = JSON.stringify({
  apiBaseUrl: process.env.API_BASE_URL || '/api/v1',
  requestTimeoutMs: Number(process.env.REQUEST_TIMEOUT_MS || 10000),
})

const server = createServer(async (req, res) => {
  const url = req.url || '/'

  if (url.startsWith('/config/runtime-config.json')) {
    res.writeHead(200, { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' })
    res.end(runtimeConfig)
    return
  }

  const urlPath = decodeURIComponent(url.split('?')[0])
  const filePath = path.resolve(distDir, `.${urlPath === '/' ? '/index.html' : urlPath}`)

  if (!filePath.startsWith(distDir)) {
    res.writeHead(403)
    res.end('Forbidden')
    return
  }

  const file = await fs.readFile(filePath).catch(() => null)
  if (file) {
    res.writeHead(200, { 'Content-Type': mimeTypes[path.extname(filePath)] || 'application/octet-stream' })
    res.end(file)
    return
  }

  // SPA fallback
  const html = await fs.readFile(path.resolve(distDir, 'index.html')).catch(() => null)
  res.writeHead(html ? 200 : 500, { 'Content-Type': 'text/html; charset=utf-8' })
  res.end(html ?? 'Internal Server Error')
})

server.listen(port, () => console.log(`Server running on http://localhost:${port}`))
