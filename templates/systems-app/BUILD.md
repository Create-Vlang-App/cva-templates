# Build flags

Systems-oriented workloads may disable the GC:

```bash
v -gc none -prod run .
```

Use `-prod` for release binaries. See [V docs](https://github.com/vlang/v/blob/master/doc/docs.md#garbage-collection) for GC modes.
