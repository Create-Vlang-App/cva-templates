# Deployment

```bash
v -prod -o systems-app .
./systems-app
```

For smaller binaries or no-GC targets:

```bash
v -gc none -prod -o systems-app .
```

Ship the single static binary, or layer the `v-docker` extension for container images.
