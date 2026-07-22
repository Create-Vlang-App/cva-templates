#!/usr/bin/env python3
"""Scaffold a template (+ optional addons) via create-vlang-app and run health checks.

Published CLI (#24): prefer `v install create-vlang-app` when available on VPM.
Until VPM publish, set CVA_CI_CLI_SOURCE to a git URL or local path (documented in docs/MAINTENANCE_CI.md).
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))

from registry import REPO_ROOT  # noqa: E402

CLI_BIN = "create-vlang-app"
VPM_MODULE = "create-vlang-app"
DEFAULT_CLI_GIT = "https://github.com/Create-Vlang-App/create-vlang-app.git"


def fail(phase: str, message: str, code: int = 1) -> None:
    print(f"\n❌ [{phase}] {message}", file=sys.stderr)
    raise SystemExit(code)


def run(phase: str, cmd: list[str], *, cwd: Path | None = None, env: dict | None = None) -> None:
    print(f"\n▶ [{phase}] {' '.join(cmd)}")
    merged = {
        **os.environ,
        "CI": "true",
        "CVA_SKIP_GIT": os.environ.get("CVA_SKIP_GIT", "1"),
        **(env or {}),
    }
    result = subprocess.run(cmd, cwd=cwd, env=merged)
    if result.returncode != 0:
        fail(phase, f"command failed with exit code {result.returncode}", result.returncode)


def resolve_file_target(file_url: str) -> Path:
    if not file_url.startswith("file://"):
        fail("scaffold", f"URL must be file:// for path guard, got: {file_url}")
    parsed = urlparse(file_url)
    pathname = unquote(parsed.path)
    subdir_list = parse_qs(parsed.query).get("subdir")
    if subdir_list:
        return Path(pathname) / subdir_list[0]
    return Path(pathname)


def assert_template_url_exists(template_url: str) -> None:
    target = resolve_file_target(template_url)
    if not target.exists() or not target.is_dir():
        fail("scaffold", f"template path missing: {target}")
    print(f"✅ [scaffold] template path exists: {target}")


def resolve_cli_invocation() -> tuple[Path | None, list[str], str]:
    """Return optional cwd, argv prefix, and mode description."""
    if shutil.which(CLI_BIN):
        return None, [CLI_BIN], "PATH"

    cli_source = os.environ.get("CVA_CI_CLI_SOURCE", DEFAULT_CLI_GIT)
    repo_root: Path | None = None

    if cli_source.startswith("http") or cli_source.startswith("git@"):
        tmp = Path(tempfile.mkdtemp(prefix="cva-cli-"))
        run("clone-cli", ["git", "clone", "--depth", "1", cli_source, str(tmp / "cli")])
        repo_root = tmp / "cli"
    else:
        repo_root = Path(cli_source).resolve()
        if not repo_root.is_dir():
            fail("scaffold", f"CVA_CI_CLI_SOURCE path not found: {repo_root}")

    module_dir = repo_root / "modules" / "create_vlang_app"
    if module_dir.is_dir():
        return module_dir, ["v", "run", "."], f"v-run:{repo_root}"

    run("install-cli", ["v", "install", str(repo_root)])
    if shutil.which(CLI_BIN):
        return None, [CLI_BIN], f"path-install:{repo_root}"
    candidate = repo_root / CLI_BIN
    if candidate.is_file():
        return None, [str(candidate)], f"path-run:{repo_root}"
    fail("scaffold", f"cannot locate CLI in {repo_root}")


def assert_non_empty_project(project_root: Path) -> None:
    if not (project_root / "v.mod").is_file():
        fail("empty-guard", f"missing v.mod in {project_root}")
    entries = [
        name
        for name in os.listdir(project_root)
        if name not in {".git", ".ci-meta.json"}
    ]
    if len(entries) < 2:
        fail("empty-guard", f"scaffold looks empty in {project_root}")
    print(f"✅ [empty-guard] project ok ({len(entries)} top-level entries)")


def main() -> None:
    parser = argparse.ArgumentParser(description="CVA layered CI scaffold check")
    parser.add_argument("--template-url", required=True)
    parser.add_argument("--addon-url", action="append", default=[])
    parser.add_argument("--set", dest="sets", action="append", default=[])
    parser.add_argument("--workdir", default=str(REPO_ROOT / ".ci-scaffold"))
    parser.add_argument("--project-name", default="scaffold-check")
    parser.add_argument("--skip-test", action="store_true")
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args()

    assert_template_url_exists(args.template_url)

    workdir = Path(args.workdir)
    if workdir.exists():
        shutil.rmtree(workdir)
    workdir.mkdir(parents=True)
    project_root = workdir / args.project_name
    project_arg = str(project_root.resolve())

    cli_cwd, cli_cmd, mode = resolve_cli_invocation()
    print(f"ℹ [scaffold] CLI resolved via {mode}")
    if mode.startswith("v-run:") and os.environ.get("CVA_CI_ALLOW_GIT_CLI") != "1":
        print(
            "WARN: using git/path CLI install — set CVA_CI_ALLOW_GIT_CLI=1 until VPM publish (#24)",
            file=sys.stderr,
        )

    scaffold_cmd = [
        *cli_cmd,
        project_arg,
        "--template",
        args.template_url,
        "--no-interactive",
        "--no-install",
        "--force",
        "--catalog-path",
        str(REPO_ROOT / "templates.json"),
    ]
    for addon_url in args.addon_url:
        scaffold_cmd.extend(["--addons", addon_url])
    for assignment in args.sets:
        scaffold_cmd.extend(["--set", assignment])

    run("scaffold", scaffold_cmd, cwd=cli_cwd, env={"CVA_SKIP_GIT": "1"})

    if not project_root.is_dir():
        fail("scaffold", f"expected project at {project_root}")

    assert_non_empty_project(project_root)
    run("fmt", ["v", "fmt", "."], cwd=project_root)
    run("vet", ["v", "vet", "."], cwd=project_root)
    if not args.skip_test:
        run("test", ["v", "test", "."], cwd=project_root)

    print("\n✅ scaffold-check passed")
    if not args.keep:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    main()
