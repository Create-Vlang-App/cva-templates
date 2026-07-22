# HTTP API

| Method | Path | Response |
|--------|------|----------|
| GET | `/` | Plain text greeting |
| GET | `/health` | `OK` (health check) |

Extend by adding methods on `App` with `@[get]`, `@[post]`, and path attributes.
