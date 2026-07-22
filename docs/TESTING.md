# Testing

How to verify templates and extensions before opening a PR.

## Prerequisites

- V compiler (`v`) on PATH — tested with V 0.5.x
- Optional: [create-vlang-app](https://github.com/Create-Vlang-App/create-vlang-app) for end-to-end scaffold checks

## Per-template smoke (in-repo)

From the template directory:

```bash
cd templates/web-server
v fmt .
v vet .
v test .
v .
```

Repeat for each `templates/<slug>/` directory.

## Per-extension smoke

Extensions are overlays — validate file presence and syntax:

```bash
# GitHub workflow YAML
python -c "import yaml,sys; yaml.safe_load(open('extensions/github-setup/.github/workflows/ci.yml'))"

# Devcontainer JSON
python -c "import json; json.load(open('extensions/development-container/.devcontainer/devcontainer.json'))"
```

## Catalog integrity (L0)

```bash
python scripts/ci/validate-registry.py
```

Validates:

- `templates.json` against `templates.schema.json`
- On-disk directories for every registry URL
- Minimum quality bar (v.mod, tests, README)

## Scaffold check (L1–L3)

Uses `scripts/ci/run-scaffold-check.py` with `create-vlang-app`:

```bash
python scripts/ci/run-scaffold-check.py \
  --template-url "file://$(pwd)?subdir=templates/web-server" \
  --workdir /tmp/cva-scaffold
```

See [MAINTENANCE_CI.md](MAINTENANCE_CI.md) for CI matrix details.

## Full matrix locally

```bash
python scripts/ci/generate-matrix.py --layer templates
python scripts/ci/generate-matrix.py --layer extensions
python scripts/ci/generate-matrix.py --layer profiles
python scripts/ci/generate-matrix.py --layer validate-profiles
```

## CI expectations

All PRs must keep L0 green. L1–L3 run on `main` and PRs; extension layers may use `--changed-only` on PRs to limit matrix size.
