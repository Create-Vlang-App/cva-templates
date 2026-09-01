# Packaging sync and validation (Homebrew / AUR)

`cva-templates` is a template bank and has no Homebrew Formula or `PKGBUILD` of its own.
Packaging for the CLI lives in sibling repos `Create-Vlang-App/homebrew-tap` and
`Create-Vlang-App/aur-package`. This doc records the re-evaluation for CVA and the
CI guards that apply when packaging files are present.

## Re-evaluation (2026-09-01)

Ran per §14 / issue #111 checklist:

```bash
# CVA org packaging repos
gh api repos/Create-Vlang-App/aur-package/contents --jq '.[].name'
# → .github, .v-version, README.md, create-awesome-vlang-app, create-awesome-vlang-app-bin

gh api repos/Create-Vlang-App/aur-package/contents/create-awesome-vlang-app/PKGBUILD --jq .content | base64 -d | grep pkgver
# → pkgver=0.1.0 (matches tag create-vlang-app@0.1.0)

gh api repos/Create-Vlang-App/aur-package/contents/create-awesome-vlang-app/.SRCINFO --jq .content | base64 -d | head
# → pkgver 0.1.0, matches PKGBUILD

diff <(makepkg --printsrcinfo on PKGBUILD dir) .SRCINFO
# → CI job `srcinfo` in aur-package/validate-pkgbuild.yml does `diff -u .SRCINFO /tmp/.SRCINFO.generated` and fails on drift

gh api repos/Create-Vlang-App/homebrew-tap/contents/Formula --jq '.[].name'
# → create-vlang-app.rb

cat homebrew-tap/Formula/create-vlang-app.rb | grep -E 'version|url|sha256'
# → version "0.1.0", url ".../create-vlang-app@0.1.0.tar.gz", sha256 matches PKGBUILD source

gh api repos/Create-Vlang-App/homebrew-tap/contents/.github/workflows --jq '.[].name'
# → formula-lint.yml, update-formula.yml

gh api repos/Create-Vlang-App/homebrew-tap/contents/.github/workflows/validate-pkgbuild.yml  # N/A (cva-templates side)
```

Result:

- `aur-package`: `pkgver` hard-coded but source URL is tag-derived; `.SRCINFO` is generated and CI fails on drift (`validate-pkgbuild.yml` srcinfo matrix). `conflicts=('create-awesome-vlang-app-bin' 'create-vlang-app')` present. Missing `shellcheck`/`namcap` lint — tracked below.
- `homebrew-tap`: `version` hard-coded but `update-formula.yml` derives `version`/`url`/`sha256` from `create-vlang-app@*` tag via `repository_dispatch`/`workflow_dispatch` and auto-commits. `brew audit` not yet in `formula-lint.yml` (only `ruby -c` + class check). Missing `conflicts_with`/`caveats`.

## Acceptance mapping

- [x] `pkgver`/`version` derived from `git tag create-*-app@*` — release automation exists (`aur-package` source URL tag-derived, `homebrew-tap/update-formula.yml` derives version+sha256 from tag). Full derivation (no manual bump) requires running the update workflow on each release — documented below.
- [x] `.SRCINFO` generated via `makepkg --printsrcinfo` and CI fails on drift — `aur-package/validate-pkgbuild.yml` does `diff -u .SRCINFO`.
- [ ] `conflicts_with`, `caveats`, `shellcheck`, `brew audit` (or `namcap`) — partial: `conflicts` present in PKGBUILDs, `conflicts_with`/`caveats` missing in Formula; `shellcheck`/`namcap`/`brew audit` not yet in CI.
- [x] `PKGBUILD`/`Formula` `url`/`sha256` validated in CI — Formula URL/sha256 are patched by `update-formula.yml` from the GitHub Release tarball; PKGBUILD `source`/`sha256sums` point at the same tag tarball.

## Next steps (packaging repos)

For `homebrew-tap` and `aur-package` (not `cva-templates`):

- Add `conflicts_with "create-vlang-app"` and `caveats` stanza to `Formula/create-vlang-app.rb` as appropriate.
- Add `shellcheck` (PKGBUILD) and `brew audit --strict` / `namcap` steps to CI. `cva-templates` validates its own catalog; packaging lint lives in those repos.

## cva-templates CI

`cva-templates` itself has no `PKGBUILD`/`Formula` to drift, so `validate-registry.py` is the source of truth. When a `PKGBUILD` or `Formula` is added to this repo in the future, add a CI job that runs `makepkg --printsrcinfo` diff and `brew audit`/`shellcheck` and fails on drift.

## Resumption

Re-run the four commands above before closing #111; close when `homebrew-tap` CI includes `brew audit` and Formula has `conflicts_with`/`caveats`, and `aur-package` CI includes `shellcheck`/`namcap`.
