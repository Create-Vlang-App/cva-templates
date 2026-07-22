# Template quality checklist (M1)

Local copy of the bank [TEMPLATE_QUALITY_M1](../../docs/TEMPLATE_QUALITY_M1.md) bar.

## Required

- [x] README documents run / test
- [x] Health route `GET /health` with feature helpers in `health/`
- [x] Feature-level tests (`health/health_test.v`)
- [x] `.env.example` documents port
- [x] Root: `AGENTS.md`, `CONTRIBUTING.md`, `QUALITY.md`
- [x] Docs suite: STRUCTURE, API, CONFIGURATION, TESTING, DEPLOYMENT
- [x] `_module_template/` scaffold present

## Extension slots (catalog slugs)

| Slug | Role |
|------|------|
| `github-setup` | GitHub Actions + setup-v |
| `v-docker` | Dockerfile + compose |
| `v-postgres` / `v-sqlite` | DB samples |
| `development-container` | Dev container |
| `v-fmt-vet` | Makefile + pre-commit |

```bash
create-vlang-app my-api \
  --template web-server \
  --addons github-setup \
  --addons v-docker \
  --no-interactive --force
```
