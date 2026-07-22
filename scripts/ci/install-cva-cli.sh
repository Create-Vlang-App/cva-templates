#!/usr/bin/env bash
# Install create-vlang-app into PATH for bank CI (published binary first).
set -euo pipefail

TAG="${CVA_CLI_RELEASE_TAG:-create-vlang-app@0.1.0}"
ASSET="${CVA_CLI_ASSET:-create-vlang-app-linux-x86_64}"
DEST="${CVA_CLI_INSTALL_DIR:-${RUNNER_TEMP:-/tmp}/cva-cli-bin}"
URL="https://github.com/Create-Vlang-App/create-vlang-app/releases/download/${TAG}/${ASSET}"

mkdir -p "$DEST"

add_to_path() {
  export PATH="${DEST}:${PATH}"
  if [[ -n "${GITHUB_PATH:-}" ]]; then
    echo "${DEST}" >> "${GITHUB_PATH}"
  fi
}

echo "▶ [cva-cli] fetching ${URL}"
if curl -fsSL "$URL" -o "${DEST}/create-vlang-app"; then
  chmod +x "${DEST}/create-vlang-app"
  add_to_path
  create-vlang-app --version
  echo "✅ [cva-cli] installed from GitHub Release ${TAG}"
  exit 0
fi

echo "⚠ [cva-cli] release asset unavailable; building from git clone" >&2
CLONE="${RUNNER_TEMP:-/tmp}/create-vlang-app-src"
rm -rf "$CLONE"
git clone --depth 1 https://github.com/Create-Vlang-App/create-vlang-app.git "$CLONE"
(
  cd "$CLONE"
  make build
)
cp "${CLONE}/create-vlang-app" "${DEST}/create-vlang-app"
chmod +x "${DEST}/create-vlang-app"
add_to_path
create-vlang-app --version
echo "✅ [cva-cli] built from git main (interim until Release assets are stable)"
