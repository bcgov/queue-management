# Appointment Booking App

A React 19 + TypeScript app for Service BC, using React Router v8 with SSR and static prerendering for the locations page.

## Prerequisites

- Node.js 22+
- npm 10+

## Local Development

```bash
cd appointment-booking
npm install
npm run dev
```

Open `http://localhost:5173/locations` (or `/` which redirects there).

### Run Checks

```bash
npm run ci:check
```

### Build for Production

```bash
npm run build
npm run start
```

The `/locations` route is prerendered at build time for SEO.

---

## Docker

From the repository root:

```bash
docker compose up --build appointment-booking
```

Or manually:

```bash
docker build -t appointment-booking .
docker run -p 5173:8080 appointment-booking
```

---

## License

MIT + Apache-2.0 (for BC Gov design system components)

See `LICENSE` file and run `npm run license-check` to verify all dependencies comply.
