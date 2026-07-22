# Project structure

```text
.
├── main.v              # veb App + route methods (framework constraint)
├── main_test.v
├── health/             # feature module: response helpers
│   ├── health.v
│   └── health_test.v
├── v.mod
├── README.md
└── docs/
    ├── README.md
    ├── PROJECT_STRUCTURE.md
    ├── TESTING.md
    ├── API.md
    ├── CONFIGURATION.md
    └── DEPLOYMENT.md
```

## Feature modules (V-native)

V resolves `import health` to a top-level `health/` directory. Nested paths like `src/features/health/` are **not** importable without custom `-path` flags, so this template keeps feature modules at the project root.

`veb` route methods must remain methods on `App` in `main.v`. Business/response helpers live in `health/`.

Generated projects may add `cva.config.json`, `.github/workflows/`, and other extension overlays.
