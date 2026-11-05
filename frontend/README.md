# The Q staff frontend

Vue 2.7 application using Vite for development and production builds.

## Requirements

- Node.js 24 (Docker uses 24.21.0)
- npm 11
- Access to the configured API and Keycloak environment

Supported browsers: the latest two versions of Chrome, Edge, Firefox,
and Safari. Internet Explorer is not supported.

## Install and run

From the frontend directory:

```bash
npm ci
npm run dev
```

For builds that do not need Cypress or Puppeteer browser binaries:

```bash
CYPRESS_INSTALL_BINARY=0 PUPPETEER_SKIP_DOWNLOAD=true npm ci
```

The development server runs at http://localhost:8082.
`npm run serve` is an alias for starting Vite.

Development and build hooks run `src/version.js` to update version metadata.

## Configuration

Build-time settings can be supplied in `.env.local`:

| Variable | Default |
| --- | --- |
| VITE_API_URL | /api/v1/ |
| VITE_SOCKET_URL | Empty; uses the application's default socket handling |
| VITE_REFRESH_TOKEN_SECONDS_LEFT | 180 |
| VITE_KEYCLOAK_JSON_URL | /static/keycloak/keycloak.json |

VITE_* values are embedded during the build and are visible to the browser.
Do not put secrets in them. Changing container environment variables after
building does not change these values.

Runtime configuration remains separate:

- `/config/configuration.json`
- `/static/keycloak/keycloak.json`

For local development, provide these under `public/` at their corresponding
paths. Do not commit environment-specific copies. The Docker build excludes
these local files; deployment must supply the required runtime configuration.

## Local API and WebSocket proxy

Vite forwards `/api` and `/socket.io` requests to:

https://test-theq.apps.silver.devops.gov.bc.ca

The `/api` proxy supports WebSockets and rewrites their Origin header to the
test backend origin. This is a local development workaround for the backend's
origin validation. Keep the development server bound to localhost.

Vite's development proxy is not included in the production image.
Production API and WebSocket routing must be provided by the deployment.

## Build and checks

```bash
npm run build
npm run lint
npm run test:unit
```

The production artifact is `dist/`.

Run timezone tests in both environments:

```bash
TZ=America/Vancouver npm run test:unit
TZ=UTC npm run test:unit
```

Unit tests use Jest and ts-jest directly, without Vue CLI.
`npm test` runs the same configured unit suite as `npm run test:unit`.

`npm run preview` serves the built artifact for inspection. It does not
reproduce the complete OpenShift deployment or its runtime configuration.

## Deployment

The build sets NODE_OPTIONS=--max-old-space-size=4096 because the
production bundle exceeded Node's default heap limit in OpenShift.
The build container currently has a 7 GiB memory limit.

OpenShift uses a Docker build with `contextDir: frontend` and
`dockerfilePath: Dockerfile`.

The Dockerfile builds with Node 24.21.0 and npm ci, then copies dist into
/app in the Nginx 1.31.8 image. Nginx listens on port 8080 and falls back to
index.html for SPA routes.

The BuildConfig's Git repository and ref determine which revision is built.

## Compatibility and remaining work

- Vue CLI and Webpack have been removed.
- The unused smartboard UI and vue-video-player dependency were removed.
- Camunda's Vue components require the legacy TypeScript decorator transform
  in vite.config.mts. This is unrelated to legacy browser support.
- Camunda/FormIO dependencies require Node API compatibility code in the
  browser, supplied by vite-plugin-node-polyfills.
- jsonwebtoken is explicitly included in Vite dependency optimization for
  CommonJS interoperability.
- FormIO still brings core-js 3 transitively. Direct legacy browser polyfill
  imports were removed, but the strict no-polyfills requirement remains
  unresolved until this dependency is updated or replaced.
- Dependency warnings remain for Font Awesome Sass, FormIO CSS,
  vm-browserify eval usage, and bundle size.
- The local admin screen has a deferred redirect/CORS issue.
- Production-image validation and manual regression testing remain required.
- Camunda uses STOMP over a browser socket. An exact-match Vite alias
  redirects `stompjs` to a local adapter for its browser implementation,
  preserving the default export without loading Node-only TCP/WebSocket
  adapters.
- Node API compatibility packages are supplied transitively by
  vite-plugin-node-polyfills through node-stdlib-browser. The application
  does not import these packages directly, so redundant root dependency
  declarations were removed. Required compatibility code remains bundled
  for the Camunda/FormIO integration.