# vsl-plotting

Adds a CI-safe `vsl.plot` helper for `vsl-starter`. Unit tests build a scatter plot
without calling interactive `show()`.

## Overlay module

Ships as a named module `plotting/` (`import plotting`) so multiple domain addons do not collide under `src/`.

## Layout

Overlay files live under `template/` and are merged onto the selected base template. This README stays at the extension root.

## Verify after scaffold

```bash
v test .
```
