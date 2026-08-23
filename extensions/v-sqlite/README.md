# v-sqlite

SQLite environment sample for web-server, cli and library templates.

## Files

- `.env.example` — `SQLITE_PATH` variable
- `config.v.example` — helper to read the path in V code

Compatible with templates: `web-server`, `cli-app`, `systems-app`, `library-starter`.

## Layout

Overlay files live under `template/` and are merged onto the selected base template. This README stays at the extension root.

## Verify after scaffold

```bash
v test .
```
