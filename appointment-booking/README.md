# Appointment Booking App

A React 19 + TypeScript appointment booking interface built for BC Gov, featuring server-side rendering (SSR), automated tests, and OpenShift deployment readiness.

## Prerequisites

- Node.js 22+
- npm 10+

For database and backend setup, follow the instructions in the [root README](../README.md).

## Local Development

### Install dependencies

```bash
cd appointment-booking
npm install
```

### Start the frontend

```bash
# Default: proxies /api/v1 to http://localhost:5000
npm run dev

# If your local API runs on a different port (e.g. 5100 on macOS where port 5000 is reserved by mDNS):
npm run dev:local
```

Open `http://localhost:5173`. If that port is in use, the server automatically falls back to `5174`.

### Frontend-only (without backend)

The frontend starts without a running backend. API calls to `/api/v1/*` will fail gracefully until the backend is running.

### Run Checks

```bash
# Run everything at once (lint + type-check + test + build + license)
npm run ci:check

# Optional: run checks individually
npm run test
npm run test:watch
npm run lint
npm run type-check
npm run license-check
```

### Build for Production

```bash
# Compile TypeScript, build client & server
npm run build

# Output in ./dist/
# - dist/client/  (browser assets)
# - dist/server/  (SSR entry point)

# Run production build locally
NODE_ENV=production node server.js
# Opens at http://localhost:5173
```

---

## Docker

### Build Image

```bash
docker build -t appointment-booking:latest .
```

### Run Container

```bash
docker run -p 5173:5173 \
  -e API_BASE_URL=http://api-service/api/v1 \
  -e NODE_ENV=production \
  appointment-booking:latest
```

**Note:** Use `host.docker.internal` on macOS/Windows to access localhost from container. On Linux, use the Docker network or actual IP.

### Run with Docker Compose

```bash
docker-compose up appointment-booking
```

(Assumes compose.yaml exists with service definition)

---

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `NODE_ENV` | `development` | Controls production vs development mode |
| `PORT` | `5173` | Server listen port |
| `FALLBACK_PORT` | `PORT + 1` | Fallback port when `PORT` is already in use (dev) |
| `API_PROXY_TARGET` | `http://localhost:5000` | Backend URL for Vite's `/api/v1` dev proxy (**dev only**) |
| `API_BASE_URL` | `/api/v1` | API base URL served to the client via runtime config (**production**) |
| `REQUEST_TIMEOUT_MS` | `10000` | API request timeout in milliseconds |

### Runtime Config

The app loads configuration from `/config/runtime-config.json` endpoint (served by `server.js`):

```json
{
  "apiBaseUrl": "/api/v1",
  "requestTimeoutMs": 10000
}
```

This endpoint reads from environment variables at startup, allowing Kubernetes ConfigMaps/Secrets to drive configuration without rebuilding the image.

---

## License

MIT + Apache-2.0 (for BC Gov design system components)

See `LICENSE` file and run `npm run license-check` to verify all dependencies comply.

---

## Contributing

1. Create a feature branch
2. Make changes and run tests: `npm run test`
3. Lint and format: `npm run lint && npm run format`
4. Push and open a PR
5. GitHub Actions runs quality checks automatically
6. Merge once checks pass

---

## Links

- **BC Gov Design System:** https://github.com/bcgov/design-system
- **React Docs:** https://react.dev
- **Vite Docs:** https://vite.dev
- **TypeScript Docs:** https://www.typescriptlang.org
- **OpenShift Docs:** https://docs.openshift.com
