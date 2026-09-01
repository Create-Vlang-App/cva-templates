# vtl-nn-cpu

Tiny CPU training loop for `vtl-starter`. Uses a one-step MSE update on a single
parameter so CI stays fast (full XOR/CIFAR stay in upstream examples).

## Overlay module

Ships as a named module `nn_cpu/` (`import nn_cpu`) so multiple domain addons do not collide under `src/`.

## Layout

Overlay files live under `template/` and are merged onto the selected base template. This README stays at the extension root.

## Verify after scaffold

```bash
v test .
```
