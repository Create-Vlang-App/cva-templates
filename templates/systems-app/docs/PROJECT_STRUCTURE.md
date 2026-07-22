# Project structure

```text
.
├── main.v
├── main_test.v
├── checksum/
│   ├── checksum.v
│   └── checksum_test.v
├── _module_template/
├── BUILD.md
├── AGENTS.md
├── CONTRIBUTING.md
├── .env.example
├── QUALITY.md
├── v.mod
├── README.md
└── docs/
```

Feature modules live at the project root (`import checksum` → `checksum/`).
