# Published CLI in CI

L1–L3 scaffold jobs install `create-vlang-app` via `scripts/ci/install-cva-cli.sh`:

1. Download the GitHub Release binary (`create-vlang-app@0.1.0` / `create-vlang-app-linux-x86_64` by default).
2. Else try `v install --git https://github.com/Create-Vlang-App/create-vlang-app`.
3. Else, only if `CVA_CI_ALLOW_GIT_CLI=1`, clone the CLI repo for `v run` fallback.

Do **not** set `CVA_CI_ALLOW_GIT_CLI=1` on push/PR/schedule. Use it only for `workflow_dispatch` emergencies while Release/VPM are unavailable.

Override tag/asset with `CVA_CLI_RELEASE_TAG` / `CVA_CLI_ASSET` when validating a newer release.
