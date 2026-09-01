# rxv-operators

Deepens `rxv-starter` with a filter → map → reduce style helper.

## Overlay module

Ships as a named module `operators/` (`import operators`) so multiple domain addons do not collide under `src/`.

## Layout

Overlay files live under `template/` and are merged onto the selected base template. This README stays at the extension root.

## Verify after scaffold

```bash
v test .
```
