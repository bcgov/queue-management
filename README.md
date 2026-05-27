# The Q

The Q is the Service BC platform for managing in-person office flow, appointments, smartboard and digital signage displays, outbound notifications, and related service delivery workflows. The application is used by Service BC as well as other B.C. government ministries.

Service BC connects people with services offered by the B.C. provincial government. This application supports the day-to-day operations of Service BC locations by helping staff manage queues, appointments, exams, walk-ins, and communications across the province.

## Applications and Services

### `api`

The primary backend service for the platform. It serves the main REST API under `/api/v1` plus Socket.IO endpoints used by the staff and public frontends.

Key responsibilities include:

- Queue and citizen service flows: create and manage citizens, service requests, queue state transitions, invite and serve flows, hold flows, and completion flows.
- Office and reference data: offices, services, categories, channels, CSR state, user context, and related administrative data.
- Appointments, bookings, and walk-ins: appointment slots, appointment creation and updates, recurring bookings, walk-in queue support, and reminder-related workflows.
- Exams, rooms, and invigilators: exam scheduling, uploads, exports, room management, and invigilator management.
- Smartboard and real-time updates: smartboard data endpoints plus Socket.IO events for queue changes and office-specific live updates.
- Health endpoints: readiness and health checks for operational monitoring.

### `frontend`

The internal staff-facing Vue 2 application. Staff use it for queue management, office administration, appointments, exams, uploads, smartboard support, and optional service-flow integrations.

### `appointment-frontend`

The public-facing Vue 2 application for booking appointments, viewing booked appointments, managing account settings, handling sign-in flows, and viewing walk-in queue status.

### `appointment-booking`

The new under developement public-facing React 19 + TypeScript application for booking appointments at Service BC locations. It will eventually replace `appointment-frontend`. See [`appointment-booking/README.md`](./appointment-booking/README.md) for setup instructions.

### `notifications-api`

A separate Flask service for outbound notifications. It exposes authenticated `POST /api/v1/notifications/sms` and `POST /api/v1/notifications/email` endpoints and supports pluggable delivery providers, including GC Notify, CHES, and logging/custom implementations.

### `feedback-api`

> [!WARNING]
> `feedback-api` is deprecated, retained only for legacy compatibility, and will be removed in a future version.

This legacy Flask service accepts feedback submissions and forwards them to the older Camunda-based feedback flow.

## Technology Stack

- Backend: Python, Flask, Flask-RESTX, SQLAlchemy, Flask-Migrate, Flask-SocketIO, Marshmallow, Gunicorn, and Gevent.
- Frontend: Vue 2 , React 19 + TypeScript + Vite , Vue Router, Vuex, Vuetify, BootstrapVue, Buefy, and Axios.
- Data and integrations: PostgreSQL, Redis-backed real-time/message queue usage, MinIO for object storage, Keycloak/OIDC authentication, optional Snowplow analytics, and GC Notify/CHES/custom notification providers.
- Serving/runtime: Nginx serves built frontend assets in containerized deployments.

Older references to RabbitMQ remain in the repository, but they are not part of the current development guidance in this README.

## Development Options

This repository supports two local development workflows:

- Using a [development container](https://containers.dev/)
- Developing locally on your host machine

### Dev Container Workflow

#### Prerequisites

- Podman or another compatible Docker engine
- Visual Studio Code (or another editor with Dev Container support)
- The Dev Containers extension for VS Code

#### Steps

1. Open the repository in an editor with dev container support
2. Use the editor to reopen the project in the devcontainer
   - For example, in VS Code, click the popup prompt or use the Command Palette to select "Dev Containers: Reopen in Container"
3. Let the container build from the root `compose.yaml` definition and finish running the post-create script
4. Confirm that the container has provisioned PostgreSQL and Keycloak, and forwarded the main ports

The devcontainer now prepares local config files before API migrations/bootstrap and waits for PostgreSQL and Keycloak readiness before the post-create flow continues.
It also provisions project-local Python environments for both `api` and `notifications-api`, so the checked-in VS Code debug configurations work without extra manual setup.

#### Expected Ports

- `5000`: queue management API
- `5002`: notifications API
- `5173`: appointment booking frontend (React)
- `8080`: staff frontend
- `8081`: appointment frontend
- `8085`: Keycloak auth server
- `5432`: PostgreSQL

The devcontainer installs dependencies automatically for `api`, `notifications-api`, `frontend`, and `appointment-frontend`, applies database migrations, and may initialize seed data depending on the current database state.

### Local Host Workflow

#### Prerequisites

- Python 3.14 with `uv`
- Node.js 20 with `npm`
- PostgreSQL 16

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

   cd ./appointment-booking
   npm install
   ```

3. Create the required local config files:

   ```bash
   ./scripts/setup-local-config.sh
   ```

   This script copies the checked-in local config defaults from `.devcontainer/config`, creates missing destination directories, validates required API auth keys, and leaves any existing local files untouched.

4. Start the local auth server:

   ```bash
   docker compose up -d keycloak
   ```

   Local Keycloak details:

   - Realm: `servicebc-local`
   - Base URL: `http://localhost:8085/auth`
   - Admin console: `http://localhost:8085/auth/admin/`
   - Admin credentials: `admin` / `password`
   - Demo users: `democsr@idir`, `demoga@idir`, `admin@idir`, `citizen@bceidboth`, `citizen2@bceidboth`
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

The root `compose.yaml` is the single source of truth for local Docker services and the devcontainer. The optional `api` Compose service still serves the application on `http://localhost:5000`. It reads `api/.env`, then overrides container-only settings so it can reach the host PostgreSQL and host-run notifications API while continuing to use the local Keycloak on `http://localhost:8085/auth`.

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

Appointment booking frontend (React):

```bash
cd ./appointment-booking
npm run dev
```

Opens at `http://localhost:5173`. See [`appointment-booking/README.md`](./appointment-booking/README.md) for Docker and environment variable details.

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

## Testing

This repository includes Python/pytest suites, Artillery-based load tests, and Postman/Newman collections. The commands below assume you already completed the local setup for the relevant service and, for API-backed tests, have the local stack running.

### Pytest Suites

The main application test suite lives in `api/app/tests` and is split into a DB-free `smoke` slice and a Postgres-backed `integration` slice.

From `api`:

```bash
./scripts/run_api_smoke_tests.sh
./scripts/run_api_integration_tests.sh
./scripts/run_api_full_tests.sh
```

Equivalent direct pytest commands:

```bash
uv run pytest app/tests -m smoke -q --override-ini "addopts=--strict-markers"
uv run pytest app/tests -m integration -q --override-ini "addopts=--strict-markers" --require-integration-db
uv run pytest app/tests -q --require-integration-db
```

Additional pytest suites:

```bash
cd ./notifications-api
uv sync --group dev
uv run pytest
```

```bash
cd ./feedback-api
make setup
make test
```

### Load Tests

Load testing lives in `tests/loadtesting` and uses Artillery against the local API stack.

Initial setup:

```bash
cd ./tests/loadtesting
npm install
cp envs.example.sh envs.sh
chmod +x envs.sh profile-python.sh
```

Before running the load tests locally, start the local Keycloak realm and seed the API data:

```bash
docker compose up -d keycloak

cd ./api
uv run python manage.py db upgrade
uv run python manage.py bootstrap
```

Run the load suites from `tests/loadtesting`:

```bash
npm run tests:all
npm run tests:http
npm run tests:socket
```

Optional Python profiling commands are also available there:

```bash
npm run python:profile
npm run python:top
```

### Newman Tests

Postman collections live in `api/postman`. They target the local API and local Keycloak realm, and the checked-in local setup expects the demo users from `keycloak-local/servicebc-local-realm.json`.

Before running Newman locally, make sure the API database is migrated and bootstrapped:

```bash
cd ./api
uv run python manage.py db upgrade
uv run python manage.py bootstrap
```

Then install Newman and run the main collection from `api/postman`:

```bash
cd ./api/postman
npm install
./node_modules/newman/bin/newman.js run API_Test_TheQ_Booking.json -e postman_env.json --bail failure \
  --global-var userid=cfms-postman-operator \
  --global-var password=password \
  --global-var userid_nonqtxn=cfms-postman-non-operator \
  --global-var password_nonqtxn=password \
  --global-var client_secret=theq-local-dev-secret \
  --global-var url=http://localhost:5000/api/v1/ \
  --global-var auth_url=http://localhost:8085 \
  --global-var clientid=theq-queue-management-api \
  --global-var realm=servicebc-local \
  --global-var public_url=http://localhost:5000/api/v1/ \
  --global-var public_user_id=cfms-postman-public-user \
  --global-var public_user_password=password
```

See `api/postman/README-local-auth.md` for local auth troubleshooting details.

## Deployment

For deployment within the B.C. government, this project can be hosted on the [B.C. government Private Cloud](https://digital.gov.bc.ca/technology/cloud/private/). The platform is the B.C. Government Private Cloud PaaS, powered by Red Hat OpenShift, and is designed for hosting government applications in a managed private-cloud environment.

This repository still includes deployment artifacts under [`openshift/templates`](./openshift/templates) for platform-specific builds and deployments.

## Getting Help or Reporting an Issue

To report bugs/issues/feature requests, please file an [issue](../../issues).

## How to Contribute

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## License

This project is licensed under the Apache License, Version 2.0. See the root [`LICENSE`](./LICENSE) file for the full license text.
