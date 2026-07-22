# Publishing (VPM)

1. Set `name`, `description`, `version`, and `license` in `v.mod`.
2. Ensure the `module` name in `src/lib.v` matches the published package name.
3. Tag a release and publish via [VPM](https://vpm.vlang.io) / `v publish` when ready.
4. Document install: `v install <your-module>`.
