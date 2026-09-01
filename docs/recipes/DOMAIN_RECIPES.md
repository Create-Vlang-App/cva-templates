# Domain recipes (upstream examples)

Registered CVA addons stay small. Use these upstream galleries for depth.

## Scientific (vlang/vsl)

| Domain | Representative examples |
|--------|-------------------------|
| Linear algebra | `blas_basic_operations`, `lapack_linear_systems`, `la_triplet01` |
| Classical ML | `ml_linreg01`, `ml_kmeans`, `ml_complete_pipeline` |
| Plotting | `plot_scatter`, `plot_heatmap_golden_ratio`, `plot_json_export` |
| Signal / FFT | `fft_plot_example`, `easings_signal_shaping` |
| Geometry | `gm_basic_geometry`, `gm_trajectory_simulation` |
| GPU | `cuda/examples/*`, `vcl_opencl_basic`, `vulkan/examples/add.v` |
| Distributed | `mpi_basic_example` |

Upstream: https://github.com/vlang/vsl/tree/master/examples

## ML / tensors (vlang/vtl)

| Domain | Representative examples |
|--------|-------------------------|
| Basics | `vtl_basic_usage`, `vtl_vandermont` |
| Autograd | `autograd_backprop` |
| NN CPU | `nn_xor`, `nn_regression_sine`, `nn_cifar10_tiny_synth` |
| Datasets | `datasets_mnist`, `datasets_imdb` |
| VSL bridge | `vtl_plot_scatter_colorscale`, `vtl_opencl_vcl_support` |
| GPU | `nn_cifar10_cuda`, `nn_cifar10_vulkan` |

Upstream: https://github.com/vlang/vtl/tree/master/examples

## Reactive (ulises-jeremias/rxv)

| Domain | Representative examples |
|--------|-------------------------|
| Hello | `hello_world` |
| Creation | `02-from-slice-and-range` |
| Operators | `03-filtering`, `04-transforming-map`, `05-aggregation`, `06-combining` |
| Errors | `07-error-handling` |

Upstream: https://github.com/ulises-jeremias/rxv/tree/master/examples

## Combining vsl + vtl

Prefer addon `vtl-vsl-bridge` on `vtl-starter` rather than a combined base template.

## Quick recipes (copy-paste)

Three starter recipes for common combinations. Each shows the exact
`create-vlang-app` command and the expected verification step.

### Web server + Docker

```bash
create-vlang-app my-webapp \
  --template web-server \
  --addons docker \
  --no-interactive
cd my-webapp
make verify   # expected: fmt check, vet, tests, and docker build all pass
```

### Scientific computing + plotting (vsl)

```bash
create-vlang-app my-science \
  --template vsl-starter \
  --addons vtl-vsl-bridge \
  --no-interactive
cd my-science
make verify   # expected: vsl/vtl examples compile and the plot example runs
```

### Reactive streams (rxv operators)

```bash
create-vlang-app my-rx \
  --template rxv-starter \
  --addons github-setup \
  --no-interactive
cd my-rx
make verify   # expected: rxv operator examples (filter/transform/combine) pass
```

If a recipe does not verify cleanly, open an issue in
[`cva-templates`](https://github.com/Create-Vlang-App/cva-templates) with the
error output.

