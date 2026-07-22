#!/usr/bin/env python3
"""L0 integrity: schema, on-disk paths, and template quality bar."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from registry import (  # noqa: E402
    REPO_ROOT,
    SCHEMA_JSON,
    TEMPLATES_JSON,
    addon_dir,
    load_registry,
    load_profiles,
    on_disk_path_for_entry,
    assert_profile_valid,
    template_dir,
)

try:
    import jsonschema
except ImportError:
    jsonschema = None  # type: ignore


def validate_schema() -> list[str]:
    errors: list[str] = []
    if jsonschema is None:
        print("WARN: jsonschema not installed — skipping schema validation")
        return errors
    schema = json.loads(SCHEMA_JSON.read_text(encoding="utf-8"))
    data = json.loads(TEMPLATES_JSON.read_text(encoding="utf-8"))
    validator = jsonschema.Draft7Validator(schema)
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        path = ".".join(str(p) for p in err.path) or "(root)"
        errors.append(f"schema: {path}: {err.message}")
    return errors


def _has_vmod(path: Path) -> bool:
    return (path / "v.mod").is_file()


def _has_tests(path: Path) -> bool:
    return any(path.rglob("*_test.v"))


def _has_readme(path: Path) -> bool:
    return (path / "README.md").is_file()


REQUIRED_TEMPLATE_DOCS = ("PROJECT_STRUCTURE.md", "TESTING.md")

# M1 quality bar — expand after each template uplift (see docs/TEMPLATE_QUALITY_M1.md).
# Starts empty; Fase 2 adds "web-server", then remaining templates in Fase 3.
M1_QUALITY_ALLOWLIST: frozenset[str] = frozenset()

M1_ROOT_FILES = (
    "README.md",
    "AGENTS.md",
    "CONTRIBUTING.md",
    ".env.example",
    "QUALITY.md",
)

M1_DOCS = (
    "README.md",
    "PROJECT_STRUCTURE.md",
    "CONFIGURATION.md",
    "TESTING.md",
    "DEPLOYMENT.md",
)

# Templates that must ship docs/API.md under M1.
M1_API_DOCS_TEMPLATES = frozenset({"web-server"})

# Templates exempt from _module_template/ + feature-module layout (libraries).
M1_NO_FEATURE_MODULES = frozenset({"library-starter"})


def _has_required_docs(path: Path) -> list[str]:
    """Return missing required docs paths relative to the template root."""
    missing: list[str] = []
    docs = path / "docs"
    if not docs.is_dir():
        return ["docs/", *[f"docs/{name}" for name in REQUIRED_TEMPLATE_DOCS]]
    for name in REQUIRED_TEMPLATE_DOCS:
        if not (docs / name).is_file():
            missing.append(f"docs/{name}")
    return missing


def _has_extension_template_dir(path: Path) -> bool:
    return (path / "template").is_dir()


def _m1_quality_errors(name: str, path: Path) -> list[str]:
    """Return M1 quality bar violations for an allowlisted template."""
    errors: list[str] = []
    for filename in M1_ROOT_FILES:
        if not (path / filename).is_file():
            errors.append(f"template {name}: M1 missing {filename}")

    docs = path / "docs"
    if not docs.is_dir():
        errors.append(f"template {name}: M1 missing docs/")
    else:
        for filename in M1_DOCS:
            if not (docs / filename).is_file():
                errors.append(f"template {name}: M1 missing docs/{filename}")
        if name in M1_API_DOCS_TEMPLATES and not (docs / "API.md").is_file():
            errors.append(f"template {name}: M1 missing docs/API.md")

    if name not in M1_NO_FEATURE_MODULES:
        if not (path / "_module_template").is_dir():
            errors.append(f"template {name}: M1 missing _module_template/")
        # At least one top-level feature dir (not src/, docs/, etc.) with a test.
        reserved = {
            "src",
            "docs",
            "examples",
            "_module_template",
            ".github",
            "ci",
            "bin",
            "assets",
        }
        feature_dirs = [
            p
            for p in path.iterdir()
            if p.is_dir() and not p.name.startswith(".") and p.name not in reserved
        ]
        has_feature_test = any(
            any(d.rglob("*_test.v")) for d in feature_dirs
        )
        if not has_feature_test:
            errors.append(
                f"template {name}: M1 needs a top-level feature module with *_test.v"
            )

    return errors


def validate_on_disk(registry: dict) -> list[str]:
    errors: list[str] = []
    seen_template_names: set[str] = set()
    seen_addon_names: set[str] = set()

    for template in registry.get("templates", []):
        name = template.get("name", "")
        if name in seen_template_names:
            errors.append(f"duplicate template name: {name}")
        seen_template_names.add(name)
        directory = template_dir(template)
        if not directory:
            errors.append(f"template {name}: cannot parse url subdir")
            continue
        if directory != name:
            errors.append(f"template {name}: directory {directory} must match name slug")
        path = on_disk_path_for_entry("template", template)
        if path is None or not path.is_dir():
            errors.append(f"template {name}: missing directory {path}")
            continue
        if not _has_vmod(path):
            errors.append(f"template {name}: missing v.mod")
        if not _has_tests(path):
            errors.append(f"template {name}: missing *_test.v")
        if not _has_readme(path):
            errors.append(f"template {name}: missing README.md")
        for missing_doc in _has_required_docs(path):
            errors.append(f"template {name}: missing {missing_doc}")
        if name in M1_QUALITY_ALLOWLIST:
            errors.extend(_m1_quality_errors(name, path))

    for addon in registry.get("addons", []):
        name = addon.get("name", "")
        if name in seen_addon_names:
            errors.append(f"duplicate addon name: {name}")
        seen_addon_names.add(name)
        directory = addon_dir(addon)
        if not directory:
            errors.append(f"addon {name}: cannot parse url subdir")
            continue
        if directory != name:
            errors.append(f"addon {name}: directory {directory} must match name slug")
        path = on_disk_path_for_entry("addon", addon)
        if path is None or not path.is_dir():
            errors.append(f"addon {name}: missing directory {path}")
            continue
        if not _has_readme(path):
            errors.append(f"addon {name}: missing README.md")
        if not _has_extension_template_dir(path):
            errors.append(
                f"addon {name}: missing template/ overlay directory "
                "(extensions must use extensions/<slug>/template/)"
            )

    return errors


def validate_profiles(registry: dict) -> list[str]:
    errors: list[str] = []
    for profile in load_profiles():
        try:
            assert_profile_valid(registry, profile)
        except ValueError as exc:
            errors.append(str(exc))
    return errors


def main() -> None:
    registry = load_registry()
    errors = validate_schema() + validate_on_disk(registry) + validate_profiles(registry)
    if errors:
        print("Registry validation failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        raise SystemExit(1)
    print(f"OK: validated {TEMPLATES_JSON.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
