# Maintenance: Dependencies

> How to update, investigate, and resolve dependency conflicts in templates and extensions.
>
> Read after the top-level [MAINTENANCE_RUNBOOK.md](./MAINTENANCE_RUNBOOK.md).

---

## 1. Investigating a V dependency

Before bumping a version, verify that it exists in the VPM registry and that its V version requirement is compatible with the template's `v.mod`.

```bash
# Inspect the current module manifest
cat templates/<slug>/v.mod

# Check a published V module version (when vpm lands)
# v search <module>
# v install <module>@<version> --dry-run (when supported)

# For domain libs, check upstream tags
gh release view --repo vlang/vsl --json tagName  # etc. for vsl/vtl/rxv
gh api repos/vlang/v/tags --jq '.[].name' | head -20
gh api repos/ulises-jeremias/rxv/tags --jq '.[].name' | head -20
```

Example:

```bash
cat templates/vsl-starter/v.mod
# Module { name: 'vsl_starter' dependencies: ['vsl@v0.2.0-beta.1'] }

gh api repos/vlang/vsl/tags --jq '.[].name' | grep beta
cat templates/vtl-starter/v.mod
cat templates/rxv-starter/v.mod
```

If a version tag does not exist upstream, `v install <module>@<version>` will fail and CI will report `cannot find module`.

Key V-native notes:

- Module layout: `v.mod` at template root declares `Module { name, version, dependencies }`. See [AUTHORING.md](./AUTHORING.md).
- Domain starters pin scientific libs: `vsl-starter` → `vsl@v0.2.0-beta.1`, `vtl-starter` → `vtl@v0.2.0-beta.1` (which transitively pulls `vsl`), `rxv-starter` → `rxv@0.1.0`. See `knowledge/create-vlang-app-v-ecosystem-notes.md`.
- V compiler itself is pinned via `vlang/setup-v` in CI (`scripts/ci` workflows). The `.v-version` file at repo root (if present) is the source of truth; otherwise CI uses `stable: true` resolving to the latest stable tag (currently `0.5.2`).

---

## 2. Dependency resolution failures

### 2.1 `v install` — module version not found

**Symptom:** `cannot find module 'vsl@v9.9.9'` or similar during `v install` / `v test`.

**Common cause:** A template or extension `v.mod` pins a version that was never tagged upstream, or a typo in the dependency string.

**Fix:**

1. Verify the tag exists upstream (`gh api repos/vlang/vsl/tags` etc.).
2. Either:
   - Pin to the latest published tag (e.g. `vsl@v0.2.0-beta.1` per `vtl` manifest).
   - Drop the dependency if it is no longer needed after a major refactor.
   - Wait for upstream to publish the new version.

### 2.2 V compiler mismatch

**Symptom:** `v vet` / `v fmt` / `v test` fails with syntax or `C.open` signature errors that previously passed (e.g. `vlib/os/filelock/lib_nix.c.v:7:6: error: C function C.open was already declared`).

**Common cause:** Upstream V breaking change in `vlang/v`. `vlang/setup-v` builds V from source; a bad stable release or bootstrap toolchain change can break all L1–L3 jobs.

**Fix:**

1. Check if `vlang/v` had a recent breaking change: `gh api repos/vlang/v/commits --jq '.[0].commit.message'`.
2. Pin CI to last known good V version:
   ```yaml
   - uses: vlang/setup-v@v1
     with:
       version: weekly.2026.08  # or explicit 0.5.2
   ```
   Label the tracking issue `bug`, `ci`, `v-compiler`.
3. Reference prior handling: weekly pin pattern used by `vtl` when stable broke.

### 2.3 `v.mod` merge conflicts (core)

**Symptom:** Generated project's `v.mod` has duplicate keys or missing dependencies after merging template + addons.

**Common cause:** Two extensions declare conflicting dependency versions for the same module name.

**Fix strategies (in order):**

1. Align both sides to a mutually compatible version (cleanest).
2. Downgrade the more aggressive requirement.
3. Mark extensions as incompatible (`incompatibleWith` in `templates.json`) if they cannot coexist.

### 2.4 V toolchain version in templates

Templates declare a minimal V version implicitly via CI `vlang/setup-v`. If bumping a domain dep requires newer V syntax, update the CI `version-file: .v-version` and verify `v fmt -verify` / `v vet` still pass locally.

---

## 3. Updating dependencies

### 3.1 In an extension

1. Edit `extensions/<slug>/template/v.mod` if the extension overlays a manifest, or `extensions/<slug>/README.md` notes if it adds deps via file overlay.
2. Most extensions (e.g. `v-docker`, `github-setup`) do not add V module deps — they overlay config/CI files under `template/` to avoid polluting `v.mod`.
3. For domain addons (`vsl-plotting`, `vsl-classical-ml`, `vtl-nn-cpu`, `vtl-vsl-bridge`, `rxv-operators`): edit the partial `v.mod` and ensure `compatibleWith` in `templates.json` remains accurate.
4. Re-scaffold the extension with each compatible template:
   ```bash
   create-vlang-app my-app \
     --template "file://$PWD?subdir=templates/vsl-starter" \
     --addons "file://$PWD?subdir=extensions/vsl-plotting" \
     --no-interactive --force --no-install
   cd my-app && v fmt -verify . && v vet . && v test .
   ```

### 3.2 In a template

1. Edit `templates/<slug>/v.mod` (`dependencies: []`).
2. Use conservative pinned versions: `vsl@v0.2.0-beta.1`.
3. Sync any top-level `v.mod` `description`/`version` fields if the change is user-facing.
4. Validate locally: `v vet . && v test .`.

### 3.3 Major updates

A major dependency update is high-risk. For each major:

1. Read the upstream changelog/tag notes (`vsl`, `vtl`, `rxv`).
2. Check V version requirements (do new APIs need newer V?).
3. Test with L2 isolation for affected extension(s) and curated L3 profile(s) in `ci/profiles/`.
4. If breaking changes affect generated code, update `template/` overlay files or top-level feature modules (`health/`, `greet/`, `numerics/`, `tensor/`, etc.).

---

## 4. Lockfiles

Generated V projects do **not** commit a lockfile; `v install` resolves from `v.mod` at scaffold time. CI smoke runs `v install` fresh without a lock. If a transitive V dependency starts breaking installs:

- Pin the transitive dep explicitly in the template `v.mod`.
- Document the pin in the template `CHANGELOG`/`QUALITY.md` notes if user-visible.
- See [MAINTENANCE_SECURITY.md](./MAINTENANCE_SECURITY.md) for CVE-driven pinning.

Avoid relying on transient registry states; pin when reproducibility matters.

---

## 5. Dependabot PRs

CVA Dependabot PRs are primarily **GitHub Actions version bumps** (not V module deps — VPM not yet wired to Dependabot). Action updates are grouped via `.github/dependabot.yml`.

### 5.1 Reviewing

```bash
gh pr list --repo Create-Vlang-App/cva-templates --author "app/dependabot" --state open \
  --json number,title,mergeable,mergeStateStatus,statusCheckRollup
gh pr view <pr> --repo Create-Vlang-App/cva-templates
```

### 5.2 Rebasing if conflicted

```bash
gh pr view <pr> --repo Create-Vlang-App/cva-templates --json mergeStateStatus
# If DIRTY:
gh pr comment <pr> --repo Create-Vlang-App/cva-templates --body "@dependabot rebase"
# or close/reopen to re-trigger if comment is ignored
```

### 5.3 Merging

- Only merge if L0–L3 CI passes (`CI Integrity`, `CI Templates`, `CI Extensions`, `CI Profiles` all SUCCESS).
- Security `priority:high` CVE bumps (OSV scanner) take priority.
- If a Dependabot PR fails CI due to V compiler regression, create an issue with label `v-compiler` and pin V version before merging.
- Do **not** merge Dependabot PRs from the maintenance loop itself — comment `CI green — ready to merge.` and label `ready-to-merge` for a human to merge.

---

## 6. Tools for complex resolution

```bash
# Validate registry + M1 quality (L0)
python3 scripts/ci/validate-registry.py

# Generate CI matrices for local inspection
python3 scripts/ci/generate-matrix.py --layer templates
python3 scripts/ci/generate-matrix.py --layer extensions
python3 scripts/ci/generate-matrix.py --layer profiles

# Local scaffold smoke
python3 scripts/ci/run-scaffold-check.py \
  --template-url "file://$PWD?subdir=templates/web-server" \
  --workdir /tmp/cva-scaffold

# V toolchain checks inside a scaffolded project
v fmt -verify .
v vet .
v test .

# Check V version
v version
```

---

## 7. Checklist

- [ ] The target version tag exists for every referenced V module (`vsl`, `vtl`, `rxv`).
- [ ] V compiler version (`setup-v`) still builds — no `C.open` or bootstrap regression.
- [ ] The change is scoped to the affected template/extension.
- [ ] Local validation passes (`python3 scripts/ci/validate-registry.py`, `v vet`, `v test`).
- [ ] Full L0–L3 matrix passes for affected templates (or `gh run list --repo Create-Vlang-App/cva-templates` green).
- [ ] If security-related, the CVE is actually addressed by the bump (see OSV workflow).

