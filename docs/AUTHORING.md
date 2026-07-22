# Authoring templates and extensions

Guide for adding or updating catalog entries in `cva-templates`.

## Before you start

1. Open a GitHub issue (or pick an existing one).
2. Branch from `main`: `feat/<issue>-<slug>`.
3. One issue per PR; reference with `Closes #N`.

## Template vs extension contract

| Kind | Path | What the CLI copies |
|------|------|---------------------|
| **Template** | `templates/<slug>/` | Entire directory = new project root |
| **Extension (addon)** | `extensions/<slug>/` | Overlay from `extensions/<slug>/template/` (preferred) |

`create-vlang-app-core` resolves an extension source with `get_template_dir_path`: if a nested `template/` directory exists, that subtree is the overlay root; otherwise the extension directory itself is used (legacy). **New extensions must use `template/`.**

Keep `README.md` at `extensions/<slug>/README.md` (not inside `template/`) so authors can document merge behavior without shipping that file into user projects.

Optional guides for users belong under `extensions/<slug>/template/docs/` (for example `GITHUB_SETUP_GUIDE.md`).

## Template checklist

Create `templates/<slug>/` with:

| File | Required | Notes |
|------|----------|-------|
| `v.mod` | yes | Module name matching project convention |
| `main.v` or `src/` | yes | Compilable entry or library root |
| `*_test.v` | yes | At least one `v test` file |
| `README.md` | yes | Usage, build, run instructions |
| `docs/README.md` | yes | Docs index |
| `docs/PROJECT_STRUCTURE.md` | yes | Layout + feature conventions |
| `docs/TESTING.md` | yes | How to run tests |
| `docs/API.md` | web-server | HTTP surface |
| `docs/CONFIGURATION.md` | recommended | Flags / env / ports |
| `docs/DEPLOYMENT.md` | web-server, systems-app | Binary / container notes |

### Feature modules (V-native)

Prefer one directory per feature at the **project root** (`greet/`, `health/`, `checksum/`). V resolves `import greet` to a top-level `greet/` folder — nested `src/features/<name>/` is not importable without custom `-path`.

For `veb` apps, keep route methods on `App` in `main.v` and put helpers in a feature module.

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

Create:

```text
extensions/<slug>/
├── README.md                 # author docs (not merged)
└── template/                 # overlay root (merged)
    ├── ...                   # files copied into the project
    └── docs/                 # optional user guides
        └── SOME_GUIDE.md
```

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

## Naming rules

- Slugs: lowercase, hyphen-separated (`web-server`, `v-docker`).
- Directory name must match the `subdir` segment in the URL.
- Do not rename slugs after release without a migration note in `docs/MAINTENANCE_TEMPLATES.md`.

## Example: minimal CLI template

```text
templates/cli-app/
├── v.mod
├── main.v
├── main_test.v
├── greet/
│   ├── greet.v
│   └── greet_test.v
├── README.md
└── docs/
    ├── README.md
    ├── PROJECT_STRUCTURE.md
    ├── TESTING.md
    └── CONFIGURATION.md
```

## Example: github-setup extension

```text
extensions/github-setup/
├── README.md
└── template/
    ├── .github/workflows/ci.yml
    └── docs/GITHUB_SETUP_GUIDE.md
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
- Registry validates (L0) — includes docs + `template/` checks
- Scaffold check passes when CLI is available (L1+)

See [ARCHITECTURE.md](ARCHITECTURE.md) for merge and URL conventions.
