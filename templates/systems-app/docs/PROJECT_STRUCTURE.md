# Project structure

```text
.
├── main.v
├── main_test.v
├── checksum/          # feature module
│   ├── checksum.v
│   └── checksum_test.v
├── BUILD.md           # compiler / GC notes
├── v.mod
├── README.md
└── docs/
```

Feature modules are top-level V packages (see `checksum/`). See [BUILD.md](../BUILD.md) for `-gc none` and related flags.
