# Maintenance: Release and Publishing

> How to manage template-bank releases and coordination with the CLI.
>
> Read after the top-level [MAINTENANCE_RUNBOOK.md](./MAINTENANCE_RUNBOOK.md).

---

## 1. Release model

`cva-templates` is **not** published to npm/PyPI. Templates and addons are distributed as a GitHub-hosted catalog:

```text
https://raw.githubusercontent.com/Create-Vlang-App/cva-templates/main/templates.json
```

- The CLI (`Create-Vlang-App/create-vlang-app`) fetches `templates.json` at scaffold time (with local cache at `~/.cache/cva`).
- Merges to `main` are consumed **immediately** by the CLI's default catalog URL. See [MAINTENANCE_RUNBOOK.md](./MAINTENANCE_RUNBOOK.md) "Release coordination".
- No changeset/tag step is required for bank-only changes. A template fix on `main` is live after CI passes.

Contrast with `create-vlang-app` itself, which **does** cut releases:

- CLI repo: `Create-Vlang-App/create-vlang-app/docs/RELEASE.md` — tag `create-vlang-app@X.Y.Z` → GitHub Release binaries (`linux_amd64` required, `darwin`/`windows` optional) + `SHA256SUMS`.
- VPM publish: `Create-Vlang-App/create-vlang-app/docs/VPM_PUBLISH.md` — interim `curl|sh` via `scripts/install.sh` mirrored at `https://create-awesome-vlang-app.vercel.app/install.sh` until `v install create-vlang-app` is approved.

Do not conflate the two: a bank PR that adds a template does **not** need a CLI tag; a CLI fix does.

---

## 2. When a bank change needs CLI coordination

| Bank change | CLI coordination needed? |
|---|---|
| New template (`templates/new-slug/`) + `templates.json` entry | No — add to allowlist when M1 bar met, but existing CLI picks it up immediately |
| New addon (`extensions/new-addon/`) + `templates.json` entry + `compatibleWith`/`incompatibleWith` | No, unless it changes CLI flags or scaffold contract |
| Category rename/add (`categories[]` in `templates.json`) | **Maybe** — CLI `--category` filter and website `src/lib/schemas.ts` validation must stay in sync. Open companion issue in `create-vlang-app` and `website` |
| Schema bump (`templates.json` `name`/`url`/`kind`/`tags` fields) | **Yes** — breaking. Propose via ADR, bump L0 validator in `scripts/ci/validate-registry.py`, and update CLI `loaders` fixture |
| Slug rename (`directory != name` or URL `?subdir=` change) | **Yes** — breaking. Follow [MAINTENANCE_TEMPLATES.md](./MAINTENANCE_TEMPLATES.md) slug stability steps and coordinate `create-vlang-app` fixture + `ci/profiles/*.json` |

For breaking changes, open an issue in `Create-Vlang-App/create-vlang-app` alongside the `cva-templates` PR and link both.

---

## 3. Preparing a bank change

Before merging to `main`:

1. Ensure `main` L0–L3 CI is green: `gh run list --repo Create-Vlang-App/cva-templates --limit 10`.
2. Validate locally:
   ```bash
   pip install -r scripts/ci/requirements.txt
   python scripts/ci/validate-registry.py
   python scripts/ci/generate-matrix.py --layer templates
   python scripts/ci/generate-matrix.py --layer extensions
   python scripts/ci/generate-matrix.py --layer profiles
   ```
3. Scaffold-smoke the affected template + addon combos:
   ```bash
   create-vlang-app my-app \
     --template "file://$PWD?subdir=templates/<slug>" \
     --addons "file://$PWD?subdir=extensions/<slug>" \
     --no-interactive --force --no-install
   cd my-app && v fmt -verify . && v vet . && v test .
   ```
4. Update website schema if categories/tags changed: `Create-Vlang-App/website/src/lib/schemas.ts` and `mock-data.ts`.

---

## 4. Publishing requirements

Unlike CNA (Changesets + npm Trusted Publishing) and CPA (PyPI Trusted Publishing via OIDC), the bank has **no OIDC publish job**. Requirements are:

1. `templates.json` validates via `scripts/ci/validate-registry.py` (L0).
2. Every catalog `url` uses `?subdir=templates/<slug>` or `?subdir=extensions/<slug>` and the on-disk directory matches the `name` slug.
3. New or moved templates include `v.mod`, `README.md`, at least one `*_test.v`, and — if M1-allowlisted — the full `docs/` suite + `_module_template/` + top-level feature dir with `*_test.v` (see [TEMPLATE_QUALITY_M1.md](./TEMPLATE_QUALITY_M1.md)).
4. CI L1–L3 scaffold checks pass (or `CVA_CI_ALLOW_GIT_CLI` path when VPM not yet available, per [MAINTENANCE_CI.md](./MAINTENANCE_CI.md)).
5. No personal token publish is needed; the GitHub raw URL is public.

---

## 5. Troubleshooting

### 5.1 `templates.json` not updating for CLI users

- **Cache:** CLI caches the catalog at `~/.cache/cva` (`CVA_CACHE_DIR`). Users may need `--refresh always` or `CVA_REFRESH=always` to bypass stale cache. See CLI `docs/ENV.md`.
- **CDN:** `raw.githubusercontent.com` may lag up to a few minutes after merge. Verify via:
  ```bash
  curl -s https://raw.githubusercontent.com/Create-Vlang-App/cva-templates/main/templates.json | jq '.templates | length'
  ```
- **Website:** `website/src/lib/data.ts` fetches live with `revalidate: 3600` (hourly ISR). After merge, wait for revalidation or redeploy.

### 5.2 L0 `validate-registry.py` fails after merge

Check:

- `templates.json` `name` slug matches on-disk directory for every entry.
- New template has `v.mod`, `README.md`, `*_test.v`, `docs/PROJECT_STRUCTURE.md` + `docs/TESTING.md`.
- `incompatibleWith`/`compatibleWith` reference only known slugs (no typos).
- If `M1_QUALITY_ALLOWLIST` was extended, all M1 checks pass (`M1_ROOT_FILES`, `M1_DOCS`, `M1_API_DOCS_TEMPLATES`).

### 5.3 CLI still reports old catalog

If CLI fixture tests fail after a bank merge, update the fixture in `Create-Vlang-App/create-vlang-app` (often `tests/fixtures/templates.json` or `modules/` loader tests) and cut a CLI patch if the fixture is pinned.

---

## 6. Verifying a bank release

### 6.1 Catalog endpoint

```bash
curl -s https://raw.githubusercontent.com/Create-Vlang-App/cva-templates/main/templates.json | jq '{templates: [.templates[].name], addons: [.addons[].name], categories: [.categories[].slug]}'
python scripts/ci/validate-registry.py  # L0
```

### 6.2 Website fetch

```bash
# Schema validation (Zod in data.ts)
curl -s https://raw.githubusercontent.com/Create-Vlang-App/cva-templates/main/templates.json | python3 -c "import json,sys; j=json.load(sys.stdin); print('ok', len(j['templates']), len(j['addons']))"
```

### 6.3 CLI scaffold smoke

```bash
create-vlang-app smoke-verify \
  --template web-server --no-interactive --no-install
# or file:// URL for unreleased catalog:
create-vlang-app my-app --template "file://$PWD?subdir=templates/web-server" --no-interactive --force --no-install
cd my-app && v test .
```

If all steps pass, the catalog is live for CLI users and the website will pick it up on next revalidation.

---

## 7. When to tag a CLI release alongside a bank change

| Change | Bank PR | CLI tag needed? |
|---|---|---|
| Docs-only in `cva-templates` | Yes | No |
| New template/extension (non-breaking) | Yes | No — CLI fetches live |
| Breaking `templates.json` schema change | Yes (with ADR) | Yes — `create-vlang-app@X.Y.Z` patch to update loader/fixtures |
| CLI engine bug (scaffold, cache, `v.mod` merge) | No | Yes — `create-vlang-app@X.Y.Z` |
| Security fix in `create-vlang-app` deps | No | Yes — release quickly |

---

## 8. Checklist

- [ ] `templates.json` validated (`python scripts/ci/validate-registry.py`).
- [ ] On-disk directories match `name` slugs and `?subdir=` URLs.
- [ ] L0–L3 CI is green (`gh run list --repo Create-Vlang-App/cva-templates`).
- [ ] Website schema still validates (`src/lib/schemas.ts` if categories/tags changed).
- [ ] If breaking change, companion issue/PR exists in `Create-Vlang-App/create-vlang-app` and optionally `website`.
- [ ] No npm/PyPI OIDC steps were required — bank is GitHub-hosted.

---

## 9. References

- CNA: `Create-Node-App/cna-templates/docs/MAINTENANCE_RELEASE.md` — Changesets + npm Trusted Publishing/OIDC.
- CPA: `Create-Python-App/cpa-templates/docs/MAINTENANCE_RELEASE.md` — tag-triggered PyPI Trusted Publishing.
- CVA CLI: `Create-Vlang-App/create-vlang-app/docs/RELEASE.md`, `docs/VPM_PUBLISH.md`, `docs/DISTRIBUTION_SETUP.md`.
- Runbook: [MAINTENANCE_RUNBOOK.md](./MAINTENANCE_RUNBOOK.md) "Release coordination".

