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
