# Project structure

```text
.
├── src/
│   ├── lib.v          # module mylib (public API)
│   └── lib_test.v
├── demo/              # light feature module (sample helper)
│   ├── demo.v
│   └── demo_test.v
├── examples/
│   └── example.v
├── v.mod
├── README.md
└── docs/
```

Rename `mylib` in `v.mod` / `src/` when publishing. Keep feature experiments as top-level modules (see `demo/`) or fold them into `src/` once the public API stabilizes.
