# CVA Templates

<div align="center">

**Official templates and extensions for [create-vlang-app](https://github.com/Create-Vlang-App/create-vlang-app).**

Compose a base template with optional overlays — one command, any V stack.

[![CI Integrity](https://github.com/Create-Vlang-App/cva-templates/actions/workflows/ci-integrity.yml/badge.svg)](https://github.com/Create-Vlang-App/cva-templates/actions/workflows/ci-integrity.yml)
[![CI Templates](https://github.com/Create-Vlang-App/cva-templates/actions/workflows/ci-templates.yml/badge.svg)](https://github.com/Create-Vlang-App/cva-templates/actions/workflows/ci-templates.yml)
[![CI Extensions](https://github.com/Create-Vlang-App/cva-templates/actions/workflows/ci-extensions.yml/badge.svg)](https://github.com/Create-Vlang-App/cva-templates/actions/workflows/ci-extensions.yml)
[![CI Profiles](https://github.com/Create-Vlang-App/cva-templates/actions/workflows/ci-profiles.yml/badge.svg)](https://github.com/Create-Vlang-App/cva-templates/actions/workflows/ci-profiles.yml)
[![V](https://img.shields.io/badge/V-0.5%2B-4B6EAF?style=flat-square)](https://vlang.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Discord](https://img.shields.io/discord/1527933660764831825?style=flat-square&label=Discord&logo=discord&logoColor=white)](https://discord.gg/dwFTsR7fK2)

[CLI](https://github.com/Create-Vlang-App/create-vlang-app) · [Website](https://github.com/Create-Vlang-App/website) · [Contributing](CONTRIBUTING.md) · [Authoring](docs/AUTHORING.md)

</div>

---

## Quick start

Install the CLI from the [latest Release](https://github.com/Create-Vlang-App/create-vlang-app/releases/tag/create-vlang-app%400.1.0) (linux amd64 asset), or build from source, then scaffold:

```bash
create-vlang-app my-app \
  --template web-server \
  --addons github-setup

# Headless / CI
create-vlang-app my-app \
  --template web-server \
  --addons github-setup \
  --no-interactive --force
```

Against this checkout:

```bash
create-vlang-app ./my-app \
  --template web-server \
  --addons github-setup \
  --catalog-path templates.json \
  --no-interactive --force --no-install
```

## Available templates

| Template | Use case |
|----------|----------|
| [web-server](./templates/web-server) | HTTP API with `veb` |
| [cli-app](./templates/cli-app) | CLI with `cli` + `os` |
| [systems-app](./templates/systems-app) | Low-level / systems binary |
| [library-starter](./templates/library-starter) | Publishable V library |
| [vsl-starter](./templates/vsl-starter) | [vsl](https://github.com/vlang/vsl) scientific starter |
| [vtl-starter](./templates/vtl-starter) | [vtl](https://github.com/vlang/vtl) tensor starter |
| [rxv-starter](./templates/rxv-starter) | [rxv](https://github.com/ulises-jeremias/rxv) reactive starter |

## Extensions

Overlay roots live under `extensions/<slug>/template/`. See each extension README.

| Extension | Adds |
|-----------|------|
| [github-setup](./extensions/github-setup) | GitHub Actions + `setup-v` |
| [v-docker](./extensions/v-docker) | Dockerfile + compose |
| [v-fmt-vet](./extensions/v-fmt-vet) | Makefile + pre-commit |
| [v-postgres](./extensions/v-postgres) | Postgres compose + env |
| [v-sqlite](./extensions/v-sqlite) | SQLite config samples |
| [development-container](./extensions/development-container) | Dev container |

## Registry

Canonical catalog: [`templates.json`](./templates.json)

```text
https://raw.githubusercontent.com/Create-Vlang-App/cva-templates/main/templates.json
```

## Layout

```text
templates/<slug>/              # base project (includes docs/)
extensions/<slug>/README.md    # author docs (not merged)
extensions/<slug>/template/    # overlay merged into the project
ci/profiles/                   # L3 curated stacks
scripts/ci/                    # L0–L3 helpers
docs/                          # architecture, authoring, maintenance
```

## CI

| Workflow | Trigger | Scope |
|----------|---------|-------|
| [CI Integrity (L0)](./.github/workflows/ci-integrity.yml) | PR + `main` | Schema, paths, docs bar, extension `template/` |
| [CI Templates (L1)](./.github/workflows/ci-templates.yml) | PR + `main` | Every template via published CLI |
| [CI Extensions (L2)](./.github/workflows/ci-extensions.yml) | PR + weekly | Template × compatible addon |
| [CI Profiles (L3)](./.github/workflows/ci-profiles.yml) | PR + weekly | Curated stacks in `ci/profiles/` |

Details: [docs/TESTING.md](./docs/TESTING.md), [docs/CI_PUBLISHED_CLI.md](./docs/CI_PUBLISHED_CLI.md).

## Documentation

| File | Contents |
|------|----------|
| [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) | Bank layout, template vs extension, merge model |
| [docs/AUTHORING.md](./docs/AUTHORING.md) | Adding templates and extensions |
| [docs/TESTING.md](./docs/TESTING.md) | Local testing and CI layers |
| [docs/MAINTENANCE_RUNBOOK.md](./docs/MAINTENANCE_RUNBOOK.md) | Operator runbook |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | Contribution guide |

## Related repositories

- [create-vlang-app](https://github.com/Create-Vlang-App/create-vlang-app) — CLI + scaffolding engine
- [website](https://github.com/Create-Vlang-App/website) — docs site
- [Create-Vlang-App](https://github.com/Create-Vlang-App) — organization home

## Contributors

<a href="https://github.com/Create-Vlang-App/cva-templates/contributors">
  <img src="https://contrib.rocks/image?repo=Create-Vlang-App/cva-templates" alt="contrib.rocks"/>
</a>

Made with [contributors-img](https://contrib.rocks).

## License

[MIT](LICENSE)
