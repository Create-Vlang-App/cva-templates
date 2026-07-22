#!/usr/bin/env python3
"""Registry helpers for CVA layered CI."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATES_JSON = REPO_ROOT / "templates.json"
SCHEMA_JSON = REPO_ROOT / "templates.schema.json"
PROFILES_DIR = REPO_ROOT / "ci" / "profiles"
CVA_REPO_URL = "https://github.com/Create-Vlang-App/cva-templates"


def load_registry() -> dict[str, Any]:
    return json.loads(TEMPLATES_JSON.read_text(encoding="utf-8"))


def dir_from_url(url: str, kind: str) -> str | None:
    prefix = "templates" if kind == "template" else "extensions"
    match = re.search(rf"[?&]subdir={prefix}/([^/&]+)(?:/|&|$)", url or "")
    if match:
        return match.group(1)
    match = re.search(rf"/{prefix}/([^/]+)(?:/|$)", url or "")
    return match.group(1) if match else None


def template_dir(template: dict[str, Any]) -> str | None:
    return dir_from_url(template.get("url", ""), "template")


def addon_dir(addon: dict[str, Any]) -> str | None:
    return dir_from_url(addon.get("url", ""), "addon")


def cva_file_url(repo_root: Path, relative_subdir: str) -> str:
    return f"file://{repo_root.resolve()}?subdir={relative_subdir}"


def template_file_url(repo_root: Path, template: dict[str, Any]) -> str:
    directory = template_dir(template)
    if not directory:
        raise ValueError(f"Cannot resolve directory for template name={template.get('name')}")
    return cva_file_url(repo_root, f"templates/{directory}")


def addon_file_url(repo_root: Path, addon: dict[str, Any]) -> str:
    directory = addon_dir(addon)
    if not directory:
        raise ValueError(f"Cannot resolve directory for addon name={addon.get('name')}")
    return cva_file_url(repo_root, f"extensions/{directory}")


def github_template_url(template: dict[str, Any]) -> str:
    directory = template_dir(template)
    if not directory:
        raise ValueError(f"Cannot resolve directory for template name={template.get('name')}")
    return f"{CVA_REPO_URL}?subdir=templates/{directory}"


def github_addon_url(addon: dict[str, Any]) -> str:
    directory = addon_dir(addon)
    if not directory:
        raise ValueError(f"Cannot resolve directory for addon name={addon.get('name')}")
    return f"{CVA_REPO_URL}?subdir=extensions/{directory}"


def find_template_by_dir(registry: dict[str, Any], directory: str) -> dict[str, Any] | None:
    for template in registry.get("templates", []):
        if template_dir(template) == directory:
            return template
    return None


def find_addon_by_name(registry: dict[str, Any], name: str) -> dict[str, Any] | None:
    for addon in registry.get("addons", []):
        if addon.get("name") == name:
            return addon
    return None


def addon_compatible_with_template(addon: dict[str, Any], template: dict[str, Any]) -> bool:
    compatible = addon.get("compatibleWith") or []
    if not compatible:
        return True
    return template.get("name") in compatible


def has_incompatibility(selected: list[dict[str, Any]], candidate: dict[str, Any]) -> bool:
    candidate_names = {candidate["name"]}
    selected_names = {a["name"] for a in selected}
    for addon in selected:
        for slug in addon.get("incompatibleWith") or []:
            if slug in candidate_names:
                return True
        for slug in candidate.get("incompatibleWith") or []:
            if slug in selected_names:
                return True
    return False


def load_profiles() -> list[dict[str, Any]]:
    if not PROFILES_DIR.is_dir():
        return []
    profiles: list[dict[str, Any]] = []
    for path in sorted(PROFILES_DIR.glob("*.json")):
        profile = json.loads(path.read_text(encoding="utf-8"))
        profiles.append({**profile, "_file": path.name})
    return profiles


def resolve_profile_addons(registry: dict[str, Any], profile: dict[str, Any]) -> list[dict[str, Any]]:
    addons: list[dict[str, Any]] = []
    for name in profile.get("addons") or []:
        addon = find_addon_by_name(registry, name)
        if not addon:
            raise ValueError(f'Profile {profile.get("id")}: unknown addon name "{name}"')
        addons.append(addon)
    return addons


def assert_profile_valid(
    registry: dict[str, Any], profile: dict[str, Any]
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    template = find_template_by_dir(registry, profile["templateDir"])
    if not template:
        raise ValueError(
            f'Profile {profile.get("id")}: unknown templateDir "{profile.get("templateDir")}"'
        )
    addons = resolve_profile_addons(registry, profile)
    selected: list[dict[str, Any]] = []
    for addon in addons:
        if not addon_compatible_with_template(addon, template):
            raise ValueError(
                f'Profile {profile.get("id")}: addon "{addon["name"]}" '
                f'incompatible with template "{template["name"]}"'
            )
        if has_incompatibility(selected, addon):
            raise ValueError(
                f'Profile {profile.get("id")}: incompatible addons involving {addon["name"]}'
            )
        selected.append(addon)
    return template, addons


def on_disk_path_for_entry(kind: str, entry: dict[str, Any]) -> Path | None:
    directory = template_dir(entry) if kind == "template" else addon_dir(entry)
    if not directory:
        return None
    folder = "templates" if kind == "template" else "extensions"
    return REPO_ROOT / folder / directory
