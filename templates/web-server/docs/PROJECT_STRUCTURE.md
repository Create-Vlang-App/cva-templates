# Project structure

```text
.
├── main.v                 # veb App + route methods (framework constraint)
├── main_test.v
├── health/                # feature module: response helpers
│   ├── health.v
│   └── health_test.v
├── _module_template/      # copy-paste scaffold for new features
├── AGENTS.md
├── CONTRIBUTING.md
├── .env.example
├── QUALITY.md
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

V resolves `import health` to a top-level `health/` directory. Nested paths like `src/features/health/` are **not** importable without custom `-path` flags.

`veb` route methods must remain methods on `App` in `main.v`. Business/response helpers live in feature modules.
