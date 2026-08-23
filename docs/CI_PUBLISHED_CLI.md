# Published CLI in CI

L1–L3 scaffold jobs install `create-vlang-app` via `scripts/ci/install-cva-cli.sh`:

1. Download the GitHub Release binary (`create-vlang-app@0.1.0` / `create-vlang-app-linux-x86_64` by default) from `https://github.com/Create-Vlang-App/create-vlang-app/releases/download/${TAG}/${ASSET}`.
2. Else build from `git clone --depth 1 https://github.com/Create-Vlang-App/create-vlang-app.git` and `make build` (fallback while Release assets stabilize).

The fallback is automatic — no `CVA_CI_ALLOW_GIT_CLI` gate or `v install --git` step. The gate `CVA_CI_ALLOW_GIT_CLI` is only used by `scripts/ci/run-scaffold-check.py` for optional `v run` fallbacks in local debugging, not by `install-cva-cli.sh`.

Override tag/asset with `CVA_CLI_RELEASE_TAG` / `CVA_CLI_ASSET` and install directory with `CVA_CLI_INSTALL_DIR` when validating a newer release:

```bash
CVA_CLI_RELEASE_TAG=create-vlang-app@0.2.0 bash scripts/ci/install-cva-cli.sh
```

See `scripts/ci/install-cva-cli.sh` for the canonical implementation.
