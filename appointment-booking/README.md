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
docker compose up appointment-booking
```

Open `http://localhost:5173`.

> The frontend requires the backend API and supporting services (database, Keycloak) to be running. See the [root README](../README.md) for instructions.

### Build and run manually

```bash
docker build -t appointment-booking .

docker run -p 5173:5173 \
  -e API_BASE_URL=http://localhost:5000/api/v1 \
  appointment-booking
```

---

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `PORT` | `5173` | Server listen port |
| `API_BASE_URL` | `/api/v1` | API base URL sent to the browser via runtime config |
| `REQUEST_TIMEOUT_MS` | `10000` | API request timeout in milliseconds |

### Runtime Config

`server.js` exposes `/config/runtime-config.json` at startup, which the React app fetches to get its configuration. This allows the same Docker image to be deployed to different environments without rebuilding.

```json
{
  "apiBaseUrl": "/api/v1",
  "requestTimeoutMs": 10000
}
```

---

## License

MIT + Apache-2.0 (for BC Gov design system components)

See `LICENSE` file and run `npm run license-check` to verify all dependencies comply.
