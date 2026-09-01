# Redis Guide

This addon ships a stubbed `redis` module (`import redis`) so you can start without a live Redis.

## Config

Set `REDIS_URL` in `.env` (see `.env.example`).

```bash
REDIS_URL=redis://localhost:6379/0
```

## Usage

```v
import redis

mut client := redis.new_memory_client()
client.set('hello', 'world')
val := client.get('hello') or { 'missing' }
```

Replace `MemoryClient` with a real client when ready; keep the `RedisClient` interface to avoid coupling tests to a live server.

## Compose (optional)

Add to your `docker-compose.yml`:

```yaml
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```
