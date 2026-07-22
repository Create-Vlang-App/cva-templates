# vsl-starter

Minimal [vlang/vsl](https://github.com/vlang/vsl) app scaffolded by create-vlang-app.

## Setup

```bash
v install vsl
v run .
v test .
```

## What you get

- `v.mod` with a real `vsl` dependency
- A tiny `vsl.la` matrix example (`matrix_trace`)
- Unit test covering the helper

## Domain catalog

This is the **Scientific Computing Starter (vsl)** base. Add capabilities via CVA addons
(see `docs/DOMAIN_AUTHORING.md` in cva-templates). Do not treat vsl/vtl as mutually exclusive —
compose `vtl-vsl-bridge` when you need both.
