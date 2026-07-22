# Project structure

```text
.
├── src/                   # entrypoint (module main)
│   ├── main.v
│   └── main_test.v
├── pipeline/              # reactive feature module
│   ├── pipeline.v
│   └── pipeline_test.v
├── demo/
├── _module_template/
├── AGENTS.md
├── CONTRIBUTING.md
├── .env.example
├── QUALITY.md
├── v.mod
├── README.md
└── docs/
```

Entry lives under `src/` (`v.mod` `subdirs`). Feature modules stay at the **project root** so `import pipeline` works without custom `-path`.
