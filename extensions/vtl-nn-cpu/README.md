# vtl-nn-cpu

Tiny CPU training loop for `vtl-starter`. Uses a one-step MSE update on a single
parameter so CI stays fast (full XOR/CIFAR stay in upstream examples).

## Overlay module

Ships as a named module `nn_cpu/` (`import nn_cpu`) so multiple domain addons do not collide under `src/`.

## Verify after scaffold

```bash
v test .
```
