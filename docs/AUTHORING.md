# Authoring templates and extensions

Guide for adding or updating catalog entries in `cva-templates`.

## Before you start

1. Open a GitHub issue (or pick an existing one).
2. Branch from `main`: `feat/<issue>-<slug>`.
3. One issue per PR; reference with `Closes #N`.

## Template vs extension decision tree

Ask: **Is this a complete starter project, or an optional overlay on an existing base?**

| Choose | When |
|--------|------|
| **Template** (`templates/<slug>/`) | New project root users scaffold with `--template`. Owns `v.mod`, entrypoint, baseline tests. |
| **Extension** (`extensions/<slug>/`) | Optional capability merged onto a base (CI, Docker, DB, domain helpers). Must not replace the base. |

**Do not** ship a new capability as a base template when an overlay addon is enough.
Align with CNA/CPA: bases stay lean; addons compose.

## Template vs extension contract

| Kind | Path | What the CLI copies |
|------|------|---------------------|
| **Template** | `templates/<slug>/` | Entire directory = new project root |
| **Extension (addon)** | `extensions/<slug>/` | Overlay from `extensions/<slug>/template/` (preferred) |

`create-vlang-app-core` resolves an extension source with `get_template_dir_path`: if a nested `template/` directory exists, that subtree is the overlay root; otherwise the extension directory itself is used (legacy). **New extensions must use `template/`.**

Keep `README.md` at `extensions/<slug>/README.md` (not inside `template/`) so authors can document merge behavior without shipping that file into user projects.

Optional guides for users belong under `extensions/<slug>/template/docs/` (for example `GITHUB_SETUP_GUIDE.md`).

### Overlay `.append` semantics

When the overlay includes `docs/README.md.append` (or other `*.append` files), the CLI
**appends** that content to the existing file in the scaffolded project instead of
overwriting it. Prefer `.append` for docs indexes so wave-1 and domain addons do not
clobber the base `docs/README.md`.

### `incompatibleWith`

Declare `incompatibleWith: ["other-addon"]` in `templates.json` **only** when two
addons would collide on the same overlay paths (for example both write
`.github/workflows/ci.yml`). Do not invent soft conflicts.

## Template checklist (baseline L0)

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

## Template checklist (M1)

See [TEMPLATE_QUALITY_M1.md](./TEMPLATE_QUALITY_M1.md). Summary:

| File | Notes |
|------|-------|
| `AGENTS.md`, `CONTRIBUTING.md`, `.env.example`, `QUALITY.md` | Root |
| `docs/CONFIGURATION.md`, `docs/DEPLOYMENT.md` | All M1 templates |
| `docs/API.md` | `web-server` only |
| `_module_template/` + ≥1 feature module | Apps / domain bases |

M1 is enforced via `M1_QUALITY_ALLOWLIST` in `scripts/ci/validate-registry.py`.

### Feature modules (V-native)

Prefer one directory per feature at the **project root** (`greet/`, `health/`, `checksum/`).
V resolves `import greet` to a top-level `greet/` folder — nested `src/features/<name>/`
is not importable without custom `-path`.

Ship `_module_template/` next to real features so users can copy-paste a new module.

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
        ├── SOME_GUIDE.md
        └── README.md.append  # preferred for index updates
```

Bank `README.md` should include a **Verify after scaffold** section (commands users run
after enabling the addon).

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

### Domain addons

Prefer **named modules** under the overlay (for example `template/plotting/`) instead of
flat `template/src/*.v` with `module main`, so merges do not collide across addons.
See [DOMAIN_AUTHORING.md](./DOMAIN_AUTHORING.md).

## Naming rules

- Slugs: lowercase, hyphen-separated (`web-server`, `v-docker`).
- Directory name must match the `subdir` segment in the URL.
- **Do not rename existing addon slugs** without a migration note in
  [`docs/MAINTENANCE_TEMPLATES.md`](./MAINTENANCE_TEMPLATES.md).
- Conventions for **new** extensions only:
  - `all-*` — cross-cutting (any base)
  - `web-*` — web-server oriented
  - `vsl-*` / `vtl-*` / `rxv-*` — domain-scoped

Existing wave-1 slugs (`github-setup`, `v-docker`, `v-fmt-vet`, …) stay as-is.

## Example: minimal CLI template

```text
templates/cli-app/
├── v.mod
├── main.v
├── main_test.v
├── greet/
│   ├── greet.v
│   └── greet_test.v
├── _module_template/
│   ├── module.v
│   └── module_test.v
├── README.md
├── AGENTS.md
├── CONTRIBUTING.md
├── .env.example
├── QUALITY.md
└── docs/
    ├── README.md
    ├── PROJECT_STRUCTURE.md
    ├── TESTING.md
    ├── CONFIGURATION.md
    └── DEPLOYMENT.md
```

## Example: github-setup extension

```text
extensions/github-setup/
├── README.md
└── template/
    ├── .github/workflows/ci.yml
    └── docs/
        ├── GITHUB_SETUP_GUIDE.md
        └── README.md.append
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
- Registry validates (L0) — includes docs + `template/` checks (+ M1 for allowlisted templates)
- Scaffold check passes when CLI is available (L1+)

See [ARCHITECTURE.md](ARCHITECTURE.md) for merge and URL conventions.

## Domain catalog (scientific / ML / reactive)

See [DOMAIN_AUTHORING.md](./DOMAIN_AUTHORING.md).
