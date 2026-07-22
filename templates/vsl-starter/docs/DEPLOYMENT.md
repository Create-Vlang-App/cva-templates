# Deployment

Build a release binary from the project root:

```bash
v -prod -o app .
```

For libraries or notebooks, prefer publishing helpers via VPM or documenting `v run` recipes in the README.

Containerize with the `v-docker` addon when you need a reproducible runtime.
