# v-fmt-vet

Local format/vet hooks via pre-commit and Makefile targets.

```bash
make check
pre-commit run --all-files
```

## Layout

Overlay files live under `template/` and are merged onto the selected base template. This README stays at the extension root.
