# Maintenance — CI

Layered CI mirrors Create-Python-App `cpa-templates` (#19).

## Layers

| Layer | Workflow | Script entrypoint |
|-------|----------|-------------------|
| L0 | `ci-integrity.yml` | `validate-registry.py`, `generate-matrix.py --layer validate-profiles` |
| L1 | `ci-templates.yml` | `run-scaffold-check.py` per template |
| L2 | `ci-extensions.yml` | template × compatible addon |
| L3 | `ci-profiles.yml` | curated stacks in `ci/profiles/` |

## Local L0

```bash
pip install -r scripts/ci/requirements.txt
python scripts/ci/validate-registry.py
python scripts/ci/generate-matrix.py --layer validate-profiles
```

## Local scaffold check

```bash
export CVA_CI_CLI_SOURCE=/path/to/create-vlang-app
export CVA_CI_ALLOW_GIT_CLI=1
python scripts/ci/run-scaffold-check.py \
  --template-url "file://$(pwd)?subdir=templates/web-server" \
  --workdir /tmp/cva-scaffold
```

## Published CLI (#24)

**Target:** L1–L3 install `create-vlang-app` from VPM / GitHub Release only.

**Current gap:** VPM publish is pending. Workflows clone `create-vlang-app` and set:

```yaml
env:
  CVA_CI_ALLOW_GIT_CLI: "1"
  CVA_CI_CLI_SOURCE: /tmp/create-vlang-app
```

When `v install create-vlang-app` is available, remove the clone step and set `CVA_CI_CLI_SOURCE` unset so `run-scaffold-check.py` resolves the binary from PATH.

## Matrix generation

```bash
python scripts/ci/generate-matrix.py --layer templates
python scripts/ci/generate-matrix.py --layer extensions
python scripts/ci/generate-matrix.py --layer profiles
```

PR workflows pass `--changed-only --base-ref origin/main` for L2/L3 to limit matrix size.

## Common failures

| Failure | Fix |
|---------|-----|
| `missing v.mod` | Add `v.mod` to template |
| `cannot parse url subdir` | Use `?subdir=templates/<slug>` URLs |
| `Profile unknown addon` | Sync `ci/profiles/*.json` with `templates.json` |
| scaffold empty | Verify on-disk template directory matches catalog slug |
