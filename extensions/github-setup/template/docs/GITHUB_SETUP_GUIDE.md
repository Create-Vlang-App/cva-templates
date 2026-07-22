# GitHub setup guide

This overlay adds a V CI workflow under `.github/workflows/ci.yml`.

## What you get

- Format check (`v fmt -verify .`)
- Vet (`v vet .`)
- Tests (`v test .`)
- Compiler via [`vlang/setup-v`](https://github.com/vlang/setup-v) (`stable: true`, cache enabled)

## Customize

1. Pin a compiler with a `v.version` (or `.v-version`) file and pass it to `setup-v`.
2. Add matrix legs for additional OS targets when your project needs them.
3. Extend jobs for Docker build, release, or lint as your stack grows.

## Related

See the extension README at the overlay root for merge behavior.
