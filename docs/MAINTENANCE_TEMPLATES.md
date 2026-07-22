# Maintenance — templates

Guidance for template quality and breaking changes.

## Quality bar (L0 enforced)

Every `templates/<slug>/` must include:

- `v.mod`
- at least one `*_test.v` (anywhere under the template tree)
- `README.md`
- compilable sources (`v test .` passes)

Primary templates (e.g. `web-server`) should also maintain `docs/` suites.

## Slug stability

- Directory name **must equal** catalog `name` slug.
- URL form: `https://github.com/Create-Vlang-App/cva-templates?subdir=templates/<slug>`

Renaming slugs requires:

1. Migration note in this file
2. Coordinated `create-vlang-app` fixture update
3. Profile JSON updates under `ci/profiles/`

## Module layout (V 0.5+)

Do not rely on virtual `src/` module roots. Use `subdirs` in `v.mod`:

```v
module mylib

subdirs: ['src']
```

Place `*_test.v` files inside declared subdirs when they test code in those subdirs.

## Wave inventory

| Slug | Category |
|------|----------|
| web-server | wave-1 |
| cli-app | wave-1 |
| library-starter | wave-1 |
| systems-app | wave-1 |
| vsl-starter | growth |
| vtl-starter | growth |
| rxv-starter | growth |

## Testing checklist

```bash
cd templates/<slug>
v fmt .
v vet .
v test .
```
