# veb-static-files

Static assets addon for `web-server` (veb). Provides `static/` dir convention, docs, and a minimal test helper.

## Overlay files

- `static/` — serve via `ctx.file` or `veb` static middleware
- `docs/STATIC_GUIDE.md` — usage and routing example
- `static_files/` module — helper to resolve static paths

## Layout

Overlay files live under `template/` and are merged onto the selected base template. This README stays at the extension root.

## Verify after scaffold

```bash
test -d static
test -f docs/STATIC_GUIDE.md
v test .
```
