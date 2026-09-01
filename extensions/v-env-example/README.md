# v-env-example

Cross-cutting env documentation standardization. Ensures `.env.example` + docs snippet for common keys via append overlays.

## Overlay files

- `.env.example.append` — common keys (PORT, ENV, DATABASE_URL, REDIS_URL, etc.)
- `docs/ENV_GUIDE.md` — env key reference
- `docs/README.md.append` — link to guide

## Layout

Overlay files live under `template/` and are merged onto the selected base template. This README stays at the extension root.

## Verify after scaffold

```bash
grep -q PORT .env.example
test -f docs/ENV_GUIDE.md
```
