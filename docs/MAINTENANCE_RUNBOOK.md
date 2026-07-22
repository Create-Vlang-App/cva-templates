# Maintenance runbook

Operator guide for `Create-Vlang-App/cva-templates`.

## When CI fails

1. Identify the layer: L0 integrity, L1 templates, L2 extensions, L3 profiles.
2. Reproduce locally (see [MAINTENANCE_CI.md](MAINTENANCE_CI.md)).
3. Fix forward on a branch `fix/<issue>-<slug>` with `Closes #N`.
4. Never merge with L0 red.

## Adding catalog entries

Follow [AUTHORING.md](AUTHORING.md) and [MAINTENANCE_TEMPLATES.md](MAINTENANCE_TEMPLATES.md).

## Release coordination

Catalog changes on `main` are consumed immediately by the CLI default URL:

```text
https://raw.githubusercontent.com/Create-Vlang-App/cva-templates/main/templates.json
```

Coordinate breaking slug/URL changes with `create-vlang-app` releases.

## Escalation

| Symptom | Doc |
|---------|-----|
| Schema / missing folder | [MAINTENANCE_CI.md](MAINTENANCE_CI.md) L0 |
| Template compile failure | [MAINTENANCE_TEMPLATES.md](MAINTENANCE_TEMPLATES.md) |
| Security concern | [MAINTENANCE_SECURITY.md](MAINTENANCE_SECURITY.md) |

## Related repos

- [create-vlang-app](https://github.com/Create-Vlang-App/create-vlang-app) — CLI engine
- [vlang/setup-v](https://github.com/vlang/setup-v) — GitHub Actions V toolchain
