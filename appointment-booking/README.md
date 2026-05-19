# Appointment Booking App

A modern React 19 + TypeScript appointment booking interface built for BC Gov, featuring server-side rendering (SSR), automated tests, and OpenShift deployment readiness.

## Quick Start (clean machine)

### Prerequisites
- Node.js 22+
- npm 10+
- Docker (for local Postgres)
- `uv` (for running Python backend)

### 1. Clone and install frontend dependencies

Run from repository root:

```bash
git clone https://github.com/bcgov/queue-management.git
cd queue-management/appointment-booking
npm install --legacy-peer-deps
```

### 2. Start database

From repository root:

```bash
cd ../
docker start citz-sbc-queue-postgres-1 || docker compose up -d db
```

### 3. Start backend API first (required for API calls)

In terminal A, from repository root:

```bash
cd api
uv sync
DATABASE_HOST=127.0.0.1 \
DATABASE_PORT=5432 \
DATABASE_NAME=sbc_queue \
DATABASE_USERNAME=postgres \
DATABASE_PASSWORD=postgres \
uv run gunicorn wsgi --bind=0.0.0.0:5100 --access-logfile=- --config=gunicorn_config.py --reload --timeout=0
```

### 4. Start frontend

In terminal B, from repository root:

```bash
cd appointment-booking
npm install --legacy-peer-deps
npm run dev:local
```

Open:
- `http://localhost:5173`
- If 5173 is in use, the server automatically falls back to 5174.

### 5. Verify everything is connected

From repository root:

```bash
curl -i http://localhost:5173/config/runtime-config.json
curl -i http://localhost:5173/api/v1/healthz/
curl -i http://localhost:5173/api/v1/offices/
```

Expected: all three return `HTTP/1.1 200 OK`.

### Frontend-only checks (without backend)

If you only want to verify SSR/frontend startup, backend is not required.
In that case, `api/v1/*` calls will fail until backend is running.

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
  -e API_PROXY_TARGET=http://host.docker.internal:5100 \
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
| `API_PROXY_TARGET` | `http://localhost:5000` | Backend API URL for proxy (dev) or sidecar (prod) |
| `NODE_ENV` | `development` | Node environment (development/production) |
| `PORT` | `5173` | Server listen port |
| `FALLBACK_PORT` | `5174` | Backup port used when `PORT` is already in use |
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
