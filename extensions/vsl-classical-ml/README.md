# vsl-classical-ml

Minimal classical ML smoke on `vsl-starter` using a closed-form 1D linear fit
(no external datasets).

## Overlay module

Ships as a named module `classical_ml/` (`import classical_ml`) so multiple domain addons do not collide under `src/`.

## Layout

Overlay files live under `template/` and are merged onto the selected base template. This README stays at the extension root.

## Verify after scaffold

```bash
v test .
```
