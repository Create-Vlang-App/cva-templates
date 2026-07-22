# Project structure

```text
.
├── main.v           # cli Command wiring
├── main_test.v
├── greet/           # feature module
│   ├── greet.v
│   └── greet_test.v
├── v.mod
├── README.md
└── docs/
```

## Feature modules

Add new commands as V modules next to `greet/` (folder name = module name), then wire flags in `main.v`. Nested `src/features/<name>/` is not used because V imports require a top-level module directory.
