# Appointment Booking App

A React 19 + TypeScript appointment booking interface built for BC Gov.

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
# Proxies /api/v1 to http://localhost:5000 (default)
npm run dev

# If your local API runs on port 5100
npm run dev:local
```

Open `http://localhost:5173`. The frontend starts without a running backend — API calls will fail gracefully until the backend is running.

### Run Checks

```bash
# Run everything at once (lint + type-check + test + build + license)
npm run ci:check

# Individually
npm run test
npm run lint
npm run type-check
```

### Build for Production

```bash
npm run build
# Output in ./dist/
```

---

## Docker

### Run with Docker Compose (recommended)

From the repository root:

```bash
docker compose --profile api up --build
```

Starts the frontend, API, database, and Keycloak. Open `http://localhost:5173`.

> Note: running Docker compose will occupy port 5173. If you then run `npm run dev`, Vite will fall back to port 5174.

### Build and run manually

```bash
docker build -t appointment-booking .
docker run -p 5173:8080 appointment-booking
```

---

## Runtime Config

The app fetches `/config/runtime-config.json` on startup to get its configuration. The default file is at [`public/config/runtime-config.json`](./public/config/runtime-config.json) and is served as a static file by nginx.

In OpenShift, a ConfigMap mounts over this file to provide environment-specific values without rebuilding the image.

```json
{
  "apiBaseUrl": "http://localhost:5000/api/v1",
  "apiBaseUrl": "http://localhost:5000/api/v1",
  "requestTimeoutMs": 10000
}
```

---

## License

MIT + Apache-2.0 (for BC Gov design system components)

See `LICENSE` file and run `npm run license-check` to verify all dependencies comply.
