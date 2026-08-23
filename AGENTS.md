# AGENTS.md

This repo is the template and addon bank for [create-vlang-app](https://github.com/Create-Vlang-App/create-vlang-app).

## Key concepts

- **`templates.json`** — single registry of all templates, addons, and categories. Every entry needs `name`, `description`, `url`; `kind` (`template` | `addon`), `tags`, and optionally `compatibleWith` / `incompatibleWith`. Slugs are the `name` field and must be globally unique.
- **`compatibleWith`** — links addons to templates. A template has no `type`; an addon lists one or more template slugs in `compatibleWith`. Empty or absent means compatible with all templates. Only matching addons appear when a template is selected. `incompatibleWith` declares addons that cannot be combined due to path collisions.
- **`v.mod`** — lives in the template root, defines `Module { name, version, description, dependencies }` for `v install` / `vpm`. Some templates ship a minimal `module main` (1 line) while publishable libraries use a full module manifest.
- **`template/` subdirectory** — for addons, the overlay root. When present, CVA copies from `extensions/<slug>/template/` instead of the addon root. Keep `README.md` at `extensions/<slug>/README.md` (not inside `template/`) so author docs are not merged into user projects.
- **`.template` and `.append` semantics** — Prefer new files; the engine supports `.template` (rendered per file) and `.append` (append to existing target, e.g. `docs/README.md.append`) and copy-only merge where later layers override earlier ones.
- **`file://` addon URL** — for local testing: `file://$PWD?subdir=templates/web-server` and `file://$PWD?subdir=extensions/github-setup`. The `?subdir=` segment must match the on-disk `templates/<slug>` or `extensions/<slug>` directory.

## How to test

```sh
# Scaffold from a local checkout
create-vlang-app my-app \
  --template "file://$PWD?subdir=templates/web-server" \
  --no-interactive --force --no-install
cd my-app && v fmt -verify . && v vet . && v test .

# Add a local addon
create-vlang-app my-app \
  --template "file://$PWD?subdir=templates/web-server" \
  --addons "file://$PWD?subdir=extensions/github-setup" \
  --no-interactive --force --no-install

# Validate registry (L0)
python3 scripts/ci/validate-registry.py
```

See [docs/TESTING.md](./docs/TESTING.md) for more examples and CI details.

## Docs

| File | Contents |
|---|---|
| [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) | System overview, template vs addon, merge model |
| [docs/AUTHORING.md](./docs/AUTHORING.md) | Directory layout, `v.mod`, addons, `compatibleWith` |
| [docs/DOMAIN_AUTHORING.md](./docs/DOMAIN_AUTHORING.md) | vsl / vtl / rxv domain addons |
| [docs/TESTING.md](./docs/TESTING.md) | Local testing commands and CI layers |
| [docs/MAINTENANCE_RUNBOOK.md](./docs/MAINTENANCE_RUNBOOK.md) | Operating constraints, decision tree, maintenance index |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | How to add templates and addons |
