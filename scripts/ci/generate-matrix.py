#!/usr/bin/env python3
"""Generate CI matrices for CVA layered workflows."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from registry import (  # noqa: E402
    REPO_ROOT,
    addon_compatible_with_template,
    addon_file_url,
    assert_profile_valid,
    github_addon_url,
    github_template_url,
    load_profiles,
    load_registry,
    template_file_url,
)


def _git_changed_paths(base_ref: str | None) -> set[str]:
    if not base_ref:
        return set()
    result = subprocess.run(
        ["git", "diff", "--name-only", base_ref, "HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return set()
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def _entry_changed(kind: str, slug: str, changed: set[str]) -> bool:
    folder = "templates" if kind == "template" else "extensions"
    prefix = f"{folder}/{slug}/"
    return any(p.startswith(prefix) or p == "templates.json" for p in changed)


def templates_matrix(use_github_urls: bool, changed_only: bool, base_ref: str | None) -> list[dict[str, Any]]:
    registry = load_registry()
    changed = _git_changed_paths(base_ref) if changed_only else set()
    cells: list[dict[str, Any]] = []
    for template in registry.get("templates", []):
        slug = template["name"]
        if changed_only and changed and not _entry_changed("template", slug, changed):
            continue
        url = github_template_url(template) if use_github_urls else template_file_url(REPO_ROOT, template)
        cells.append(
            {
                "id": f"template-{slug}",
                "template": slug,
                "templateUrl": url,
            }
        )
    return cells


def extensions_matrix(use_github_urls: bool, changed_only: bool, base_ref: str | None) -> list[dict[str, Any]]:
    registry = load_registry()
    changed = _git_changed_paths(base_ref) if changed_only else set()
    cells: list[dict[str, Any]] = []
    for template in registry.get("templates", []):
        for addon in registry.get("addons", []):
            if not addon_compatible_with_template(addon, template):
                continue
            t_slug = template["name"]
            a_slug = addon["name"]
            if changed_only and changed:
                if not (
                    _entry_changed("template", t_slug, changed)
                    or _entry_changed("addon", a_slug, changed)
                ):
                    continue
            t_url = github_template_url(template) if use_github_urls else template_file_url(REPO_ROOT, template)
            a_url = github_addon_url(addon) if use_github_urls else addon_file_url(REPO_ROOT, addon)
            cells.append(
                {
                    "id": f"{t_slug}+{a_slug}",
                    "template": t_slug,
                    "addon": a_slug,
                    "templateUrl": t_url,
                    "addons": [a_url],
                }
            )
    return cells


def profiles_matrix(use_github_urls: bool, changed_only: bool, base_ref: str | None) -> list[dict[str, Any]]:
    registry = load_registry()
    changed = _git_changed_paths(base_ref) if changed_only else set()
    cells: list[dict[str, Any]] = []
    for profile in load_profiles():
        template, addons = assert_profile_valid(registry, profile)
        pid = profile["id"]
        if changed_only and changed:
            touched = any(p.startswith("ci/profiles/") for p in changed)
            touched = touched or _entry_changed("template", template["name"], changed)
            for addon in addons:
                touched = touched or _entry_changed("addon", addon["name"], changed)
            if not touched:
                continue
        t_url = github_template_url(template) if use_github_urls else template_file_url(REPO_ROOT, template)
        a_urls = [
            github_addon_url(a) if use_github_urls else addon_file_url(REPO_ROOT, a) for a in addons
        ]
        cells.append(
            {
                "id": pid,
                "template": template["name"],
                "templateUrl": t_url,
                "addons": a_urls,
                "sets": profile.get("sets") or {},
            }
        )
    return cells


def validate_profiles_layer() -> None:
    registry = load_registry()
    for profile in load_profiles():
        assert_profile_valid(registry, profile)
    print(f"OK: {len(load_profiles())} profiles validated")


def write_output(matrix: list[dict[str, Any]]) -> None:
    import os

    payload = json.dumps(matrix)
    sys.stdout.write(payload + "\n")
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        delim = "MATRIX_EOF"
        with Path(github_output).open("a", encoding="utf-8") as handle:
            handle.write(f"matrix<<{delim}\n{payload}\n{delim}\n")
            handle.write(f"count={len(matrix)}\n")
    print(f"Generated {len(matrix)} matrix cell(s)", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--layer",
        required=True,
        choices=["templates", "extensions", "profiles", "validate-profiles"],
    )
    parser.add_argument("--github-urls", action="store_true", help="Use published GitHub URLs")
    parser.add_argument("--changed-only", action="store_true")
    parser.add_argument("--base-ref", default="origin/main")
    args = parser.parse_args()

    if args.layer == "validate-profiles":
        validate_profiles_layer()
        return

    base_ref = args.base_ref if args.changed_only else None
    if args.layer == "templates":
        cells = templates_matrix(args.github_urls, args.changed_only, base_ref)
    elif args.layer == "extensions":
        cells = extensions_matrix(args.github_urls, args.changed_only, base_ref)
    else:
        cells = profiles_matrix(args.github_urls, args.changed_only, base_ref)

    write_output(cells)


if __name__ == "__main__":
    main()
