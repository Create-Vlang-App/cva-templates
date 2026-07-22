# v-docker

Multi-stage Dockerfile and compose file for V applications.

## Usage

```bash
docker compose up --build
```

Adjust exposed ports to match your template (default `8080` for web-server).

## Layout

Overlay files live under `template/` and are merged onto the selected base template. This README stays at the extension root.
