# cva-templates

Official template and extension bank for [Create Vlang App](https://github.com/Create-Vlang-App/create-vlang-app).

## Catalog

- [`templates.json`](templates.json) — registry consumed by the CLI (`--list-templates`, `--list-addons`)
- [`templates.schema.json`](templates.schema.json) — JSON Schema for the catalog

Default catalog URL:

```text
https://raw.githubusercontent.com/Create-Vlang-App/cva-templates/main/templates.json
```

## Layout

```text
templates/<slug>/     # base project templates (v.mod + src + tests)
extensions/<slug>/    # optional layers merged on top of a template
ci/profiles/          # curated L3 CI profile definitions
scripts/ci/           # layered CI helpers (L0–L3)
docs/                 # architecture, authoring, maintenance runbooks
```

## Quick start (local scaffold)

```bash
create-vlang-app ./my-app \
  --template web-server \
  --addons github-setup \
  --catalog-path templates.json \
  --no-interactive --force --no-install
```

## Docs

| Doc | Purpose |
|-----|---------|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Bank layout and merge model |
| [docs/TESTING.md](docs/TESTING.md) | How to test templates locally |
| [docs/AUTHORING.md](docs/AUTHORING.md) | Adding templates and extensions |
| [docs/MAINTENANCE_RUNBOOK.md](docs/MAINTENANCE_RUNBOOK.md) | Operator runbook |

## License

MIT — see [LICENSE](LICENSE).
