# Agent notes

This project was scaffolded by [create-vlang-app](https://github.com/Create-Vlang-App/create-vlang-app).

## Layout

- Prefer **top-level feature modules** (`import greet` → `greet/`). Do not nest under `src/features/`.
- Copy `_module_template/` when adding a new feature.
- Keep docs under `docs/` in sync with behavior changes.

## Verify

```bash
v fmt -w .
v vet .
v test .
```
