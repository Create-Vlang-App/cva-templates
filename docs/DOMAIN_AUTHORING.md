# Domain authoring guide (scientific / ML / reactive)

How to grow the CVA scientific stack without a combinatorial template catalog.
Parent epic: [#61](https://github.com/Create-Vlang-App/cva-templates/issues/61).
Philosophy mirror: [CPA #71](https://github.com/Create-Python-App/cpa-templates/issues/71).

## Decision tree: template vs addon vs recipe

| Question | Template | Addon | Recipe |
|----------|----------|-------|--------|
| New project topology / primary paradigm? | Yes | No | No |
| Optional capability on an existing base? | No | Yes | Maybe |
| One of 50+ upstream demos (chart type, algorithm)? | No | No | Yes (link upstream) |
| GPU / dataset download required? | Never by default | Opt-in addon, out of default CI | Doc-only |

**Do not** add `plot-*-starter` or `ml-*-starter` templates per algorithm.
**Do not** add a fourth `vsl-vtl-combined` base — compose `vtl-starter` + `vtl-vsl-bridge`.

## Categories

| Slug | Bases | Notes |
|------|-------|-------|
| `scientific` | `vsl-starter` | Numerics, stats, geometry, plots (via addons) |
| `machine-learning` | `vtl-starter` | Tensors, autograd, NN (vtl; may pull vsl) |
| `reactive` | `rxv-starter` | Observable pipelines |

Display names lead with **domain**; library names stay in tags (`vsl`, `vtl`, `rxv`).

## Bases (locked at 3)

| Slug | UX name | Role |
|------|---------|------|
| `vsl-starter` | Scientific Computing Starter | Classical scientific app topology |
| `vtl-starter` | ML / Tensor Starter | Tensor/ML app topology |
| `rxv-starter` | Reactive App Starter | Reactive streams topology |

## Addon MVP set

| Addon | Compatible bases | Purpose |
|-------|------------------|---------|
| `vsl-plotting` | vsl-starter | `vsl.plot` wiring; no GUI in unit tests |
| `vsl-classical-ml` | vsl-starter | One linreg-style smoke |
| `vtl-nn-cpu` | vtl-starter | Tiny CPU NN loop (CI-safe) |
| `vtl-vsl-bridge` | vtl-starter | Tensor → VSL plot bridge |
| `rxv-operators` | rxv-starter | filter/map/reduce beyond `just` |

GPU (`cuda`/`vulkan`) addons are documented later and stay out of default L3.

## CI rules

1. Default tests are CPU-only and fast.
2. Do not call interactive `plt.show()` in unit tests — build plots / export instead.
3. L3 profiles stay small (`scientific-default`, `ml-cpu-default`, `reactive-default`, `ml-plot-bridge`).
4. Never stack every scientific addon in one job.

## Recipes

Long-tail demos live in `docs/recipes/DOMAIN_RECIPES.md` with links to upstream
`examples/` in vlang/vsl, vlang/vtl, and ulises-jeremias/rxv.

## Named modules (required)

Domain addon overlays must ship **named modules** (for example `template/plotting/`) rather than flat `template/src/*.v` with `module main`. This avoids merge collisions when composing multiple addons.
