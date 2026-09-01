# vtl-vsl-bridge

Compose VTL + VSL without a combined base template: build plot series from tensors.

## Overlay module

Ships as a named module `vsl_bridge/` (`import vsl_bridge`) so multiple domain addons do not collide under `src/`.

## Layout

Overlay files live under `template/` and are merged onto the selected base template. This README stays at the extension root.

## Verify after scaffold

```bash
v test .
```
