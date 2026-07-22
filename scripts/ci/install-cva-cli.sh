#!/usr/bin/env bash
# Install create-vlang-app into PATH for bank CI (published binary first).
set -euo pipefail

TAG="${CVA_CLI_RELEASE_TAG:-create-vlang-app@0.1.0}"
ASSET="${CVA_CLI_ASSET:-create-vlang-app-linux-x86_64}"
DEST="${CVA_CLI_INSTALL_DIR:-${RUNNER_TEMP:-/tmp}/cva-cli-bin}"
URL="https://github.com/Create-Vlang-App/create-vlang-app/releases/download/${TAG}/${ASSET}"

mkdir -p "$DEST"
echo "▶ [cva-cli] fetching ${URL}"
if curl -fsSL "$URL" -o "${DEST}/create-vlang-app"; then
  chmod +x "${DEST}/create-vlang-app"
  echo "${DEST}" >> "${GITHUB_PATH:-/dev/null}"
  export PATH="${DEST}:${PATH}"
  create-vlang-app --version
  echo "✅ [cva-cli] installed from GitHub Release ${TAG}"
  exit 0
fi

echo "⚠ [cva-cli] release asset unavailable; trying v install --git" >&2
if v install --git https://github.com/Create-Vlang-App/create-vlang-app 2>/dev/null; then
  if command -v create-vlang-app >/dev/null 2>&1; then
    create-vlang-app --version
    echo "✅ [cva-cli] installed via v install --git"
    exit 0
  fi
fi

if [[ "${CVA_CI_ALLOW_GIT_CLI:-0}" == "1" ]]; then
  echo "⚠ [cva-cli] emergency git clone (CVA_CI_ALLOW_GIT_CLI=1)" >&2
  git clone --depth 1 https://github.com/Create-Vlang-App/create-vlang-app.git /tmp/create-vlang-app
  echo "CVA_CI_CLI_SOURCE=/tmp/create-vlang-app" >> "${GITHUB_ENV:-/dev/null}"
  exit 0
fi

echo "❌ [cva-cli] could not install published CLI; set CVA_CI_ALLOW_GIT_CLI=1 for emergency clone" >&2
exit 1
