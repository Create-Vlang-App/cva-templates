# Contribuyendo

¡Gracias por contribuir! Este repositorio impulsa [create-vlang-app](https://github.com/Create-Vlang-App/create-vlang-app).

Para una explicación completa de cómo funcionan las plantillas (templates), extensiones (addons) y el sistema de archivos, lee [docs/AUTHORING.md](./docs/AUTHORING.md). También hay una traducción al español: [docs/AUTHORING.es.md](./docs/AUTHORING.es.md) (la versión en inglés es la canónica).

## Agregar una extensión (addon)

1. Crea `extensions/<tu-slug>/`
2. Agrega archivos para copiar en el proyecto generado (usa `template/` — obligatorio para nuevas extensiones — si quieres que solo un subconjunto se copie)
3. Regístrala en `templates.json` bajo `"addons"`:

```json
{
  "name": "Mi Extensión",
  "description": "Agrega X a tu proyecto",
  "url": "https://github.com/Create-Vlang-App/cva-templates?subdir=extensions/mi-extension",
  "kind": "addon",
  "tags": ["wave-1"],
  "compatibleWith": ["web-server", "cli-app"]
}
```

`compatibleWith` es opcional; úsalo solo cuando el addon depende de bases específicas (por ejemplo `vsl-starter`).

## Agregar una plantilla (template)

1. Crea `templates/<tu-slug>/` con `v.mod`, `main.v` o `src/`, y al menos un `*_test.v`
2. Asegúrate de incluir `README.md`, `docs/README.md` y los archivos de calidad según [docs/AUTHORING.md](./docs/AUTHORING.md)
3. Regístrala en `templates.json` bajo `"templates"`:

```json
{
  "name": "mi-plantilla",
  "description": "Starter V para X",
  "url": "https://github.com/Create-Vlang-App/cva-templates?subdir=templates/mi-plantilla",
  "kind": "template",
  "tags": ["wave-1"]
}
```

Valida localmente:

```bash
python scripts/ci/validate-registry.py
v test ./templates/mi-plantilla
```

## Mensajes de commit

Usa [commits convencionales](https://www.conventionalcommits.org/es): `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`.

## Checklist de PR

- [ ] El nombre del directorio coincide con el slug en `templates.json` (`subdir` del `url`)
- [ ] `url` apunta a la ruta correcta en la rama `main` (`?subdir=templates/<slug>` o `?subdir=extensions/<slug>`)
- [ ] `name` es globalmente único entre templates y addons
- [ ] Todos los campos requeridos presentes: `name`, `description`, `url`, `kind`, `tags`
- [ ] `compatibleWith` solo cuando hay dependencia real de bases (por ejemplo `vsl-starter`, `vtl-starter`, `rxv-starter`)
- [ ] `tags` incluye `wave-1` o `domain` según corresponda
- [ ] La extensión usa `template/` como raíz de overlay y `README.md` queda fuera (no se copia)
- [ ] Probado localmente — mira [docs/TESTING.md](./docs/TESTING.md)

## ¿Preguntas?

Abre un [issue](https://github.com/Create-Vlang-App/cva-templates/issues) o inicia una [discussion](https://github.com/Create-Vlang-App/cva-templates/discussions).

## Nota sobre Contribuciones

La versión **canónica** es la versión en inglés (`CONTRIBUTING.md`). Se mantiene un **resumen breve en español** aquí abajo para crear un acceso rápido al proceso de contribución para hispanohablantes.

## Resumen Rápido para Hispanohablantes

**Para iniciar una contribución:**

1. **Clona el repo** desde `https://github.com/Create-Vlang-App/cva-templates`
2. **Lee `docs/AUTHORING.md`** para entender cómo funcionan plantillas y extensiones
3. **Crea una extensión (addon)**
   - Crea una carpeta nueva: `extensions/<tu-slug>/`
   - Agrega archivos a copiar en el proyecto dentro de `template/` (obligatorio para nuevas extensiones); `README.md` queda en la raíz del addon
   - Regístrala en `templates.json` bajo `"addons"` siguiendo el formato de ejemplo
4. **Crea una plantilla (template)**
   - Crea una carpeta nueva: `templates/<tu-slug>/`
   - Incluye `v.mod`, entry point (`main.v` o `src/`), al menos un `*_test.v`, `README.md` y docs en `docs/`
   - Regístrala en `templates.json` bajo `"templates"`
5. **Sigue las reglas**:
   - Usa commits convencionales (por ejemplo, `feat:`, `fix:`, `docs:`)
   - Verifica la checklist de PR en la versión en inglés
6. **Prueba localmente**
   - Ejecuta `python scripts/ci/validate-registry.py` y `v test .` dentro de la plantilla
   - Consulta [docs/TESTING.md](./docs/TESTING.md) para guías completas

**Para más ayuda:** Abre un issue o discussion en el repo.
