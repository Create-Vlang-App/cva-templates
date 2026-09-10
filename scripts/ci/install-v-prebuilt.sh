#!/usr/bin/env bash
# Install a pinned prebuilt V compiler into PATH for bank CI.
#
# Why not vlang/setup-v: the pinned setup-v action builds V from source on
# every cold-cache run (its dist predates the prebuilt support in its src),
# and upstream source builds are currently broken by vc/V skew
# (vlang/vc floats under `make fresh_vc`). The official prebuilt release
# asset for the pinned version is deterministic and checksum-verified.
# See https://github.com/Create-Vlang-App/cva-templates/issues/119
set -euo pipefail

VERSION="$(tr -d ' \t\r\n' < "${GITHUB_WORKSPACE:-.}/.v-version")"
DEST="${V_INSTALL_DIR:-${HOME}/vlang/vlang_linux_x64}"

# SHA-256 of v_linux.zip per V version, mirrored from the pinned checksums in
# vlang/setup-v src/checksums.ts (verified locally with `sha256sum`).
checksum_for() {
  case "$1" in
    0.5.2) echo "86caf9e70c3342d48ef19eb4f6c47b709f18c90ae86255520d5c29df6b482e23" ;;
    *) echo "unsupported V version for prebuilt install: $1 (update checksum_for)" >&2; return 1 ;;
  esac
}

OS="$(uname -s)"
ARCH="$(uname -m)"
if [[ "$OS" != "Linux" || "$ARCH" != "x86_64" ]]; then
  echo "unsupported platform for prebuilt install: ${OS}/${ARCH}" >&2
  exit 1
fi

ASSET="v_linux.zip"
URL="https://github.com/vlang/v/releases/download/${VERSION}/${ASSET}"
EXPECTED="$(checksum_for "$VERSION")"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

echo "▶ [v] fetching ${URL}"
curl -fsSL "$URL" -o "${WORK}/${ASSET}"

echo "▶ [v] verifying sha256"
ACTUAL="$(sha256sum "${WORK}/${ASSET}" | awk '{print $1}')"
if [[ "$ACTUAL" != "$EXPECTED" ]]; then
  echo "checksum mismatch for ${ASSET} (${VERSION}): expected ${EXPECTED}, got ${ACTUAL}" >&2
  exit 1
fi

rm -rf "$DEST"
mkdir -p "$DEST"
unzip -q "${WORK}/${ASSET}" -d "$WORK/unzipped"
# Prebuilt zips wrap contents in a single top-level `v/` directory.
mv "$WORK"/unzipped/v/* "$DEST/"

export PATH="${DEST}:${PATH}"
if [[ -n "${GITHUB_PATH:-}" ]]; then
  echo "${DEST}" >> "${GITHUB_PATH}"
fi

v version
echo "✅ [v] installed prebuilt V ${VERSION} (${ASSET}, sha256 verified)"
