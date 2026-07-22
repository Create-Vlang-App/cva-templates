# Configuration

| Setting | Default | Notes |
|---------|---------|-------|
| Listen port | `8080` | Passed to `veb.run` in `main.v` |
| Bind address | all interfaces | Change in `main` if you need localhost-only |

Environment-based port selection is a common follow-up:

```v
port := os.getenv_opt('PORT') or { '8080' }.int()
veb.run[App, Context](mut app, port)
```

Use the `v-docker` / `v-postgres` / `v-sqlite` extensions for container and database env samples.
