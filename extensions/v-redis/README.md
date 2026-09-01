# v-redis

Redis-oriented addon for web-server and systems apps. Provides config sample, docs guide, and a stubbed client so unit tests run without a live Redis.

## Overlay module

Ships as a named module `redis/` (`import redis`) so multiple addons do not collide.

## Usage

```bash
# env
REDIS_URL=redis://localhost:6379/0
# compose (optional) – add a redis service to your compose file
```

See `docs/REDIS_GUIDE.md` for connection and stub usage.

## Layout

Overlay files live under `template/` and are merged onto the selected base template. This README stays at the extension root.

## Verify after scaffold

```bash
v test .
test -f docs/REDIS_GUIDE.md
grep -q REDIS_URL .env.example
```
