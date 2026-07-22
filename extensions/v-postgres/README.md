# v-postgres

Postgres compose overlay and environment variables.

## Usage

```bash
docker compose -f docker-compose.postgres.yml up -d
```

Merge with `v-docker` when containerizing the app and database together.

## Layout

Overlay files live under `template/` and are merged onto the selected base template. This README stays at the extension root.
