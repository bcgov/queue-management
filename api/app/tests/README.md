# API Test Suite Guide

This suite covers the active API surface used by `/frontend` and
`/appointment-frontend`. The suite is split into a DB-free `smoke`
slice and a Postgres-backed `integration` slice.

## Supported Run Modes

From the API root:

```sh
cd /Users/csampson/Developer/Repositories/queue-management/api
```

Smoke-only, DB-free:

```sh
./scripts/run_api_smoke_tests.sh
```

Integration-only, fail fast if disposable Postgres is unavailable:

```sh
./scripts/run_api_integration_tests.sh
```

Full suite, including the default line and branch coverage reports:

```sh
./scripts/run_api_full_tests.sh
```

Equivalent direct pytest commands:

```sh
uv run pytest app/tests -m smoke -q --override-ini "addopts=--strict-markers"
uv run pytest app/tests -m integration -q --override-ini "addopts=--strict-markers" --require-integration-db
uv run pytest app/tests -q --require-integration-db
```

Marker-specific runs still work during local debugging:

```sh
uv run pytest app/tests -m contracts -q --override-ini "addopts=--strict-markers"
uv run pytest app/tests -m flows -q --override-ini "addopts=--strict-markers"
uv run pytest app/tests -m validation -q --override-ini "addopts=--strict-markers"
uv run pytest app/tests -m "contracts and integration" -q --override-ini "addopts=--strict-markers" --require-integration-db
```

## Smoke Vs Integration

`smoke` is the reliable local gate. It does not require disposable Postgres and
should stay free of DB-dependent skips.

`integration` is the seeded disposable-Postgres suite. It covers the auth,
contracts, flows, validation, and DB-backed modernization checks that exercise
the live application stack.

The `--require-integration-db` flag makes Postgres dependency failures loud. If
the DB cannot be created or reached, pytest exits immediately instead of
collapsing the integration slice into a wall of skips.

If you intentionally want a best-effort local run that allows integration tests
to skip when Postgres is unavailable, `uv run pytest app/tests -q` still works.
That mode is useful for quick local debugging, but it should not be treated as
rewrite-readiness coverage because DB-backed skips can mask missing regression
signal.

The default pytest configuration now records both line and branch coverage and
writes reports to `htmlcov/` and `coverage.xml`. The explicit marker-focused
commands above override `addopts` so local debugging stays fast and uncluttered.

## Harness Layout

| Path | Purpose |
| --- | --- |
| `conftest.py` | Thin pytest plugin loader plus marker/collection policy |
| `fixtures/db.py` | Disposable Postgres, app boot, migrations, and seeded data |
| `fixtures/auth.py` | Authenticated client factories and identity fixtures |
| `fixtures/smoke.py` | Minimal Flask helpers for DB-free smoke tests |
| `contracts/schemas.py` | Shared response schema registry for contract tests |
| `contracts/conftest.py` | Contract validation helper only |
| `helpers/appointments.py` | Reminder and appointment test helpers |
| `helpers/exams.py` | Exam integration test helpers |
| `auth/auth_support.py` | Route builders, seeded auth helpers, integration stubs |

## Test Coverage

- Auth boundaries across public, mixed-role, authenticated-only, and
  internal-only routes
- Frontend-facing contracts for appointments, users, bookings, exams,
  citizens, service requests, and reference data
- Explicit frontend route contracts for `/csrs/`, `/rooms/?office_id=...`,
  `/invigilators/offsite/`, and `/smardboard/side-menu/<office_number>`
- Office-scoped service-list coverage for `/services/?office_id=...`,
  including filtering of deleted services and stable frontend ordering
- CSR dashboard coverage for `/csrs/me/`, including `attention_needed`,
  `active_citizens`, and rewrite-critical feature flags consumed by
  `/frontend`
- Core appointment, draft, booking, exam, queue, and CSR flows
- Current-office recurring booking delete coverage, including same-office
  deletion rules and the current-day `<= 5am` preservation exception
- Walk-in and smartboard behavior coverage for queue grouping, payload shaping,
  and reminder side effects used by `/appointment-frontend` and smartboard UIs
- Direct availability-service coverage for DST grouping, `soonest_appointment`,
  blackout pruning, DLKT slot caps, and overlap checks
- Reminder payload contracts and behavior for email and SMS reminder jobs
- Service-request creation branches for missing payloads, category rejection,
  first-service ticket numbering, and additional-service Snowplow transitions
- Service refresh behavior for GA and SUPPORT roles
- Active exam integration flows for BCMP create/status, transfer, download, and
  invigilator email
- Pesticide and group-exam creation coverage, including candidate
  normalization, non-SBC office reassignment, and exam export filter variants
- Exam export coverage for fail-fast validation, localized CSV timestamps,
  blank room/invigilator fields, and designate-vs-office-scoped exports
- DB-free websocket smoke coverage for join-room, smartboard-room, and cache
  handlers
- Flask 3, Marshmallow 4, WTForms, timezone, and SQLAlchemy modernization smoke
  coverage

## Contract Strictness Policy

The schema registry in `contracts/schemas.py` treats frontend-owned
envelopes and stable nested objects as closed contracts by using
`additionalProperties: False`.

Strict by default for:

- appointments
- public users
- bookings
- exams
- citizens and service requests
- offices, services, categories, channels, rooms, invigilators, exam types

Intentionally permissive where the payload shape is genuinely variable:

- date-keyed slot maps
- office `timeslots`
- BCMP and candidate payloads that the frontend does not treat as fixed
  contracts

`contracts/test_contract_strictness.py` guards against accidental schema
loosening by injecting unexpected fields into valid payloads and asserting that
validation fails.

## Deprecated And Out-Of-Scope Surface

The following routes should not affect rewrite-readiness scoring:

- `/feedback/`
- `/slack/`
- upload routes
- video routes

Deprecated auth coverage that still exists for upload or video routes should be
treated as cleanup follow-up, not as a blocker for the active rewrite safety
net.
