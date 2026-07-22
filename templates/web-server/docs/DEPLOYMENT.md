# Deployment

Build a single static binary:

```bash
v -prod .
./main
```

Use the `v-docker` extension for container deployment. Bind `PORT` in production reverse proxies; default listen port is `8080`.
