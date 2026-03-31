# The Q

The Q is the Service BC platform for managing in-person office flow, appointments, smartboard and digital signage displays, outbound notifications, and related service delivery workflows. The application is used by Service BC as well as other B.C. government ministries.

Service BC connects people with services offered by the B.C. provincial government. This application supports the day-to-day operations of Service BC locations by helping staff manage queues, appointments, exams, walk-ins, and communications across the province.

## Applications and Services

### `api`

The primary backend service for the platform. It provides the REST API and Socket.IO endpoints used by the staff and public frontends for queue operations, office administration, appointments, walk-ins, exams, uploads, smartboard data, and real-time updates.

### `frontend`

The internal staff-facing Vue 2 application. Staff use it for queue management, office administration, appointments, exams, uploads, smartboard support, and optional service-flow integrations.

### `appointment-frontend`

The public-facing Vue 2 application for booking appointments, viewing booked appointments, managing account settings, handling sign-in flows, and viewing walk-in queue status.

### `notifications-api`

A separate Flask service for outbound notifications. It exposes authenticated SMS and email endpoints and supports pluggable delivery providers, including GC Notify, CHES, and logging/custom implementations.

### `feedback-api`

> [!WARNING]
> `feedback-api` is deprecated, retained only for legacy compatibility, and will be removed in a future version.

This legacy Flask service accepts feedback submissions and forwards them to the older Camunda-based feedback flow.

## API Overview

The primary API is served from `api` and exposes endpoints under `/api/v1`.

- Queue and citizen service flows: create and manage citizens, service requests, queue state transitions, invite and serve flows, hold flows, and completion flows.
- Office and reference data: offices, services, categories, channels, CSR state, user context, and related administrative data.
- Appointments, bookings, and walk-ins: appointment slots, appointment creation and updates, recurring bookings, walk-in queue support, and reminder-related workflows.
- Exams, rooms, and invigilators: exam scheduling, uploads, exports, room management, and invigilator management.
- Smartboard and real-time updates: smartboard data endpoints plus Socket.IO events for queue changes and office-specific live updates.
- Health endpoints: readiness and health checks for operational monitoring.

## Supporting APIs

### `notifications-api`

The notifications service exposes:

- `POST /api/v1/notifications/sms`
- `POST /api/v1/notifications/email`

These endpoints are authenticated and are used for outbound text and email delivery.

### `feedback-api`

The legacy feedback service exposes:

- `POST /api/v1/feedback`

It exists for backward compatibility only and should not be treated as a core long-term service.

## Frontends

### Staff frontend

The [`frontend`](./frontend) application is the internal operational interface used by Service BC staff. It includes queue dashboards, admin screens, appointment and exam workflows, upload tools, smartboard support, and integrations with other line-of-business applications.

### Public appointment frontend

The [`appointment-frontend`](./appointment-frontend) application is the public web experience. It supports appointment booking, reviewing booked appointments, sign-in and account management, and walk-in queue status pages.

## Technology Stack

- Backend: Python, Flask, Flask-RESTX, SQLAlchemy, Flask-Migrate, Flask-SocketIO, Marshmallow, Gunicorn, and Gevent.
- Frontend: Vue 2, TypeScript, Vue Router, Vuex, Vuetify, BootstrapVue, Buefy, and Axios.
- Data and integrations: PostgreSQL, Redis-backed real-time/message queue usage, MinIO for object storage, Keycloak/OIDC authentication, optional Snowplow analytics, and GC Notify/CHES/custom notification providers.
- Serving/runtime: Nginx serves built frontend assets in containerized deployments.

Older references to RabbitMQ remain in the repository, but they are not part of the current development guidance in this README.

## Development Options

This repository supports two local development workflows:

- Devcontainer
- Local host

### Dev Container Workflow

#### Prerequisites

- Podman or another compatible Docker engine
- Visual Studio Code (or another editor with Dev Container support)
- The Dev Containers extension for VS Code

#### Steps

1. Open the repository in VS Code.
2. Use the Dev Containers command to reopen the project in the devcontainer.
3. Let the post-create script finish installing Python and Node dependencies.
4. Confirm that the container has provisioned PostgreSQL and forwarded the main ports.

#### Expected Ports

- `5000`: queue management API
- `5002`: notifications API
- `8080`: staff frontend
- `8081`: appointment frontend
- `5432`: PostgreSQL

The devcontainer installs dependencies automatically, applies database migrations, and may initialize seed data depending on the current database state.

### Local Host Workflow

#### Prerequisites

- Python 3.14
- `uv`
- Node.js 20
- `npm`
- PostgreSQL 16 or a compatible local PostgreSQL instance

#### Setup

1. Install backend dependencies:

   ```bash
   cd ./api
   uv sync --group dev

   cd ./notifications-api
   uv sync --group dev
   ```

2. Install frontend dependencies:

   ```bash
   cd ./frontend
   npm install

   cd ./appointment-frontend
   npm install
   ```

3. Create the required local config files from the repo's devcontainer config sources:

   ```bash
   cp ./.devcontainer/config/api/dotenv ./api/.env
   cp ./.devcontainer/config/api/client_secrets/secrets.json ./api/client_secrets/secrets.json
   cp ./.devcontainer/config/frontend/public/static/keycloak/keycloak.json ./frontend/public/static/keycloak/keycloak.json
   cp ./.devcontainer/config/frontend/public/config/configuration.json ./frontend/public/config/configuration.json
   cp ./.devcontainer/config/appointment-frontend/dotenv.local ./appointment-frontend/.env.local
   cp ./.devcontainer/config/appointment-frontend/public/config/kc/keycloak-public.json ./appointment-frontend/public/config/kc/keycloak-public.json
   cp ./.devcontainer/config/appointment-frontend/public/config/configuration.json ./appointment-frontend/public/config/configuration.json
   ```

4. Start the local auth server:

   ```bash
   docker compose up -d keycloak
   ```

   Local Keycloak details:

   - Realm: `servicebc-local`
   - Base URL: `http://localhost:8085/auth`
   - Admin console: `http://localhost:8085/auth/admin/`
   - Admin credentials: `admin` / `password`
   - Demo users: `democsr@idir`, `demoga@idir`, `admin@idir`, `citizen@bceidboth`
   - Demo user password: `password`
   - Confidential client id: `theq-queue-management-api`
   - Confidential client secret: `theq-local-dev-secret`

5. Make sure the database settings in `api/.env` point to your local PostgreSQL instance.

6. Run database migrations:

   ```bash
   cd ./api
   uv run python manage.py db upgrade
   ```

#### Run Commands

Start the services in separate terminals.

Queue management API using the local Python environment:

```bash
cd ./api
uv run gunicorn wsgi --bind=0.0.0.0:5000 --access-logfile=- --config=gunicorn_config.py --reload --timeout=0
```

Queue management API using the production Dockerfile through Compose:

```bash
docker compose --profile api up --build api
```

The optional `api` Compose service still serves the application on `http://localhost:5000`. It reads `api/.env`, then overrides container-only settings so it can reach the host PostgreSQL and host-run notifications API while continuing to use the local Keycloak on `http://localhost:8085/auth`.

Notifications API:

```bash
cd ./notifications-api
uv run gunicorn wsgi:application --bind=0.0.0.0:5002 --access-logfile=- --config=gunicorn_config.py --reload --timeout=0
```

Staff frontend:

```bash
cd ./frontend
npm run serve
```

Appointment frontend:

```bash
cd ./appointment-frontend
npm run serve -- --port 8081
```

#### Local Config Files

These are the main local files you should expect to have in place when running the application locally:

- `api/.env`
- `api/client_secrets/secrets.json`
- `frontend/public/static/keycloak/keycloak.json`
- `frontend/public/config/configuration.json`
- `appointment-frontend/.env.local`
- `appointment-frontend/public/config/kc/keycloak-public.json`
- `appointment-frontend/public/config/configuration.json`

The checked-in local auth defaults now target the local Keycloak realm on `http://localhost:8085/auth`. If you need to switch back to the shared dev Keycloak server, update the copied local config files before starting the apps.

## Deployment

For deployment within the B.C. government, this project can be hosted on the [B.C. government Private Cloud](https://digital.gov.bc.ca/technology/cloud/private/). The platform is the B.C. Government Private Cloud PaaS, powered by Red Hat OpenShift, and is designed for hosting government applications in a managed private-cloud environment.

This repository still includes deployment artifacts under [`openshift/templates`](./openshift/templates) for platform-specific builds and deployments.

## Getting Help or Reporting an Issue

To report bugs/issues/feature requests, please file an [issue](../../issues).

## How to Contribute

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## License

This project is licensed under the Apache License, Version 2.0. See the root [`LICENSE`](./LICENSE) file for the full license text.
