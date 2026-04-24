# Local Newman Auth Notes

Use the current local Keycloak realm and client when running the Postman collections with Newman:

- Realm: `servicebc-local`
- Client ID: `theq-queue-management-api`
- Client secret: `theq-local-dev-secret`
- Auth base URL: `http://localhost:8085/auth`
- API base URL: `http://localhost:5000/api/v1/`

The checked-in local realm now gives the Newman client both local service audiences:

- `theq-queue-management-api`
- `theq-notifications-api`

That matters because appointment creation forwards the caller bearer token to `notifications-api` for email/SMS side effects. Without the notifications audience on the Newman token, the booking request can still pass while the local API logs a downstream `401` from `http://localhost:5002`.

Before running the collections, seed the local API database so the expected CSR records exist:

```bash
cd /Users/csampson/Developer/Repositories/queue-management/api
uv run python manage.py db upgrade
uv run python manage.py bootstrap
```

The legacy `account` client and `registry` realm values in older examples are not valid for the checked-in local stack.

The Postman users in `keycloak-local/servicebc-local-realm.json` need claims that match the current API token parsing:

- Internal users need `theq_username` and `identity_provider=idir`
- Public users need `theq_username`, `identity_provider=bceid`, and `display_name`
- The public user also needs non-empty `email` and `lastName` so `/users/` schema checks pass

If you already imported the local realm before pulling this change, re-import `keycloak-local/servicebc-local-realm.json` or add the `audience-theq-notifications-api` protocol mapper to client `theq-queue-management-api` manually. The Newman command does not change.

The checked-in collections now authenticate explicitly during setup and fail fast if auth or a prerequisite variable is missing. For local and CI runs, prefer `--bail failure` so one auth/setup issue does not cascade into misleading `404`, `422`, or schema failures.

Example Newman command:

```bash
cd /Users/csampson/Developer/Repositories/queue-management/api/postman
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
