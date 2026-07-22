# development-container

VS Code devcontainer with the official V Docker image.

Open the generated project in a devcontainer-enabled editor after scaffold.

## Layout

Overlay files live under `template/` and are merged onto the selected base template. This README stays at the extension root.

## Verify after scaffold

```bash
test -f .devcontainer/devcontainer.json
```
