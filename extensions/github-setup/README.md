# github-setup

Adds GitHub Actions CI using [vlang/setup-v](https://github.com/vlang/setup-v).

## Files merged

- `.github/workflows/ci.yml` — fmt, vet, and test on push/PR

## Inputs

Uses `stable: true` and action cache. Pin a compiler version with a `v.version` file in your project root.

## Layout

Overlay files live under `template/` and are merged onto the selected base template. This README stays at the extension root.

## Verify after scaffold

```bash
test -f .github/workflows/ci.yml
v fmt -w .
v vet .
v test .
```
