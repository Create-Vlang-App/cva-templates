# Static Files Guide (veb)

This addon adds a `static/` directory for serving assets from a `web-server` (veb) app.

## Structure

```
static/
├── index.html
├── style.css
└── app.js
```

## veb usage

In `main.v`, serve files:

```v
import os

@[get; path: '/static/:path...']
pub fn (app &App) static_files(mut ctx Context, path string) veb.Result {
    file := os.join_path('static', path)
    if os.exists(file) {
        return ctx.file(file)
    }
    return ctx.not_found()
}
```

Or use `veb` static middleware if configured.

## Verify

```bash
test -d static
test -f docs/STATIC_GUIDE.md
v test ./static_files
```
