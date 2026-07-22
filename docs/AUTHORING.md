# Authoring templates and extensions

Guide for adding or updating catalog entries in `cva-templates`.

## Before you start

1. Open a GitHub issue (or pick an existing one).
2. Branch from `main`: `feat/<issue>-<slug>`.
3. One issue per PR; reference with `Closes #N`.

## Template checklist

Create `templates/<slug>/` with:

| File | Required | Notes |
|------|----------|-------|
| `v.mod` | yes | Module name matching project convention |
| `main.v` or `src/` | yes | Compilable entry or library root |
| `*_test.v` | yes | At least one `v test` file |
| `README.md` | yes | Usage, build, run instructions |
| `docs/` | recommended | For primary templates (see web-server) |

Register in `templates.json`:

```json
{
  "name": "my-template",
  "description": "One-line summary",
  "url": "https://github.com/Create-Vlang-App/cva-templates?subdir=templates/my-template",
  "kind": "template",
  "tags": ["wave-1"]
}
```

Validate:

```bash
python scripts/ci/validate-registry.py
cd templates/my-template && v test .
```

## Extension checklist

Create `extensions/<slug>/` with overlay files only (workflows, Docker, env samples, hooks).

Register under `addons` in `templates.json`:

```json
{
  "name": "my-extension",
  "description": "What it adds",
  "url": "https://github.com/Create-Vlang-App/cva-templates?subdir=extensions/my-extension",
  "kind": "addon",
  "tags": ["wave-1"],
  "compatibleWith": ["web-server", "cli-app"]
}
```

Add `extensions/my-extension/README.md` explaining merge behavior and env vars.

## Naming rules

- Slugs: lowercase, hyphen-separated (`web-server`, `v-docker`).
- Directory name must match the `subdir` segment in the URL.
- Do not rename slugs after release without a migration note in `docs/MAINTENANCE_TEMPLATES.md`.

## Example: minimal CLI template

```
templates/cli-app/
├── v.mod
├── main.v
├── main_test.v
└── README.md
```

`v.mod`:

```v
module main
```

`main.v` should expose `--help` via the `cli` module and exit 0 on success.

## Example: github-setup extension

```
extensions/github-setup/
├── .github/workflows/ci.yml
└── README.md
```

Workflow must use [`vlang/setup-v`](https://github.com/vlang/setup-v) with `version-file` or `stable` inputs.

## CI profiles (L3)

Add `ci/profiles/<id>.json`:

```json
{
  "id": "web-server-github",
  "description": "Web server with GitHub CI",
  "templateDir": "web-server",
  "addons": ["github-setup"]
}
```

Run `python scripts/ci/generate-matrix.py --layer validate-profiles` before pushing.

## Review bar

- Compiles with `v` on Linux (CI canonical)
- Tests pass (`v test`)
- Registry validates (L0)
- Scaffold check passes when CLI is available (L1+)

See [ARCHITECTURE.md](ARCHITECTURE.md) for merge and URL conventions.
