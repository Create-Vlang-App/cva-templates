# Template quality bar (M1)

Enforceable maturity checklist for base templates in `cva-templates`.

Each template that opts into M1 ships a local [`QUALITY.md`](../templates/web-server/QUALITY.md)
(or equivalent under `templates/<slug>/QUALITY.md`). Maintainers keep that file in sync
when acceptance criteria change.

## Required root files

| File | Notes |
|------|-------|
| `README.md` | Usage, build, run, links to docs |
| `AGENTS.md` | Agent/contributor orientation |
| `CONTRIBUTING.md` | How to contribute to the scaffolded project |
| `.env.example` | Documented env vars (even if empty stubs) |
| `QUALITY.md` | Local copy of this bar for the template |

## Required docs/

| File | Notes |
|------|-------|
| `docs/README.md` | Docs index |
| `docs/PROJECT_STRUCTURE.md` | Layout + feature conventions |
| `docs/CONFIGURATION.md` | Flags / env / ports |
| `docs/TESTING.md` | How to run tests |
| `docs/DEPLOYMENT.md` | Binary / container / publish notes (libraries: VPM-oriented) |
| `docs/API.md` | **Only** for `web-server` (HTTP surface) |

## Feature modules (apps / domain bases)

- Prefer one directory per feature at the **project root** (`health/`, `greet/`, `numerics/`).
- V resolves `import health` to a top-level `health/` folder — never nest under `src/features/<name>/`.
- Ship `_module_template/` as a copy-paste scaffold for new features.
- At least one real feature module with `*_test.v`.

`library-starter` is exempt from app feature modules; it uses `src/` + `examples/` instead.

## L0 enforcement

`scripts/ci/validate-registry.py` applies the M1 checks only to templates listed in
`M1_QUALITY_ALLOWLIST`. Expand the allowlist after each template is uplifted and CI is green.

```bash
python scripts/ci/validate-registry.py
```

## Related

- Epic: Wave 4 README uplift + template M1
- [AUTHORING.md](./AUTHORING.md) — authoring contract
- Gold refs: CPA `fastapi-starter`, CNA `hono-starter`
