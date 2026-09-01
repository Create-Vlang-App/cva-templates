# Env Example Guide

This addon standardizes `.env.example` documentation via append overlays.

## Common keys

| Key | Example | Description |
|-----|---------|-------------|
| PORT | 8080 | HTTP port for web-server |
| ENV | development | development / production |
| DATABASE_URL | postgres://... | Primary DB URL |
| REDIS_URL | redis://localhost:6379/0 | Cache URL |
| SQLITE_PATH | ./data.db | SQLite file path |
| LOG_LEVEL | info | debug / info / warn / error |

## Usage

1. Copy `.env.example` to `.env`
2. Fill values per environment
3. Docs snippet is appended via `docs/README.md.append` so base docs are not clobbered

## Verify

```bash
grep -q PORT .env.example
test -f docs/ENV_GUIDE.md
```
