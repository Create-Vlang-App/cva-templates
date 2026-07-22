# Deployment

Build a release binary:

```bash
v -prod -o app .
```

Distribute the binary for your target OS/arch. Prefer GitHub Releases or package managers for installers.

Containerize with the `v-docker` addon when you need a reproducible runtime image.
