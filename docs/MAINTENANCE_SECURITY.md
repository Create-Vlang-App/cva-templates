# Maintenance — security

Security practices for the template bank.

## Reporting

Report vulnerabilities via GitHub Security Advisories on [Create-Vlang-App/cva-templates](https://github.com/Create-Vlang-App/cva-templates/security/advisories/new).

For CLI engine issues, report to [create-vlang-app](https://github.com/Create-Vlang-App/create-vlang-app).

## Template content

- Do not embed secrets, tokens, or production credentials in templates or extensions.
- Use `.env.example` with placeholder values only (`v-sqlite`, `v-postgres`).
- Pin third-party GitHub Actions to major versions (`@v4`, `@v1`) and review Dependabot PRs.

## Generated projects

Extensions add workflows and container configs — document required secrets in extension README files, never commit real values.

## Docker

- Base images: official `ghcr.io/vlang/vlang` and minimal runtime (`debian:bookworm-slim`).
- Avoid running scaffold containers as root in production; devcontainer uses root for simplicity only.

## CI scripts

Python helpers (`scripts/ci/`) run in GitHub Actions with `contents: read` only. They must not execute untrusted catalog URLs beyond the checked-out repo `file://` paths in CI.

## Dependency audit

Track V compiler updates via `vlang/setup-v` stable channel. Scientific templates (vsl/vtl) may add module deps — document CPU-only defaults and optional CUDA as out-of-scope for CVA CI (#29).
