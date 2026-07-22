# vtl-starter

Minimal [vlang/vtl](https://github.com/vlang/vtl) app (depends on VSL transitively).

## Setup

```bash
v install vtl
v run .
v test .
```

## What you get

- `v.mod` with a real `vtl` dependency
- A tiny `vtl.from_1d` tensor size helper
- Unit test covering the helper

## Domain catalog

This is the **ML / Tensor Starter (vtl)** base. Add capabilities via CVA addons
(see `docs/DOMAIN_AUTHORING.md` in cva-templates). Do not treat vsl/vtl as mutually exclusive —
compose `vtl-vsl-bridge` when you need both.
