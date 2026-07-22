# Project structure

```text
.
├── src/
│   ├── main.v
│   └── main_test.v
├── demo/              # light feature module
│   ├── demo.v
│   └── demo_test.v
├── v.mod
├── README.md
└── docs/
```

Domain logic starts in `src/`; extract top-level feature modules as the app grows.
