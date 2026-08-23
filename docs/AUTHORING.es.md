# Creación y mantenimiento de plantillas y extensiones

Guía para colaboradores que quieran añadir o actualizar entradas del catálogo en `cva-templates`. Mantiene paridad con [cna-templates AUTHORING.md](https://github.com/Create-Node-App/cna-templates/blob/main/docs/AUTHORING.md) y [cpa-templates AUTHORING.md](https://github.com/Create-Python-App/cpa-templates/blob/main/docs/AUTHORING.md), adaptada para V.

> **Nota sobre CI:** El repositorio define cuatro niveles de integración continua. CI Integrity (L0) valida `templates.json`, rutas en disco, barra de calidad y estructura `template/` de extensiones; CI Templates (L1) prueba cada plantilla con `v test`; CI Extensions (L2) valida combinaciones template × addon compatibles; y CI Profiles (L3) ejecuta stacks curados en `ci/profiles/`. Consulta [docs/TESTING.md](./TESTING.md) y [docs/ARCHITECTURE.md](./ARCHITECTURE.md).

## Antes de empezar

1. Abre un GitHub issue (o elige uno existente).
2. Crea tu rama desde `main`: `feat/<issue>-<slug>`.
3. Un solo issue por PR; referencia con `Closes #N`.

## Árbol de decisión: ¿plantilla o extensión?

Pregunta: **¿Es un proyecto completo o un overlay opcional sobre una base existente?**

| Elige | Cuándo |
|--------|------|
| **Template** (`templates/<slug>/`) | Nuevo proyecto que el usuario genera con `--template`. Posee `v.mod`, entrypoint, tests base. |
| **Extensión / addon** (`extensions/<slug>/`) | Capacidad opcional que se fusiona sobre una base (CI, Docker, DB, helpers de dominio). No debe reemplazar la base. |

**No** publiques una capacidad nueva como template base cuando un addon overlay es suficiente. Alineado con CNA/CPA: las bases se mantienen livianas; los addons componen.

## Contrato template vs extensión

| Tipo | Ruta | Qué copia la CLI |
|------|------|---------------------|
| **Template** | `templates/<slug>/` | Todo el directorio = nuevo root del proyecto |
| **Extensión (addon)** | `extensions/<slug>/` | Overlay desde `extensions/<slug>/template/` (preferido) |

`create-vlang-app-core` resuelve un source de extensión con `get_template_dir_path`: si existe un subdirectorio `template/` anidado, ese subárbol es el overlay root; de lo contrario usa el directorio de la extensión (legacy). **Las nuevas extensiones deben usar `template/`.**

Mantén `README.md` en `extensions/<slug>/README.md` (no dentro de `template/`) para documentar el comportamiento de merge sin incluir ese archivo en los proyectos generados.

Las guías opcionales para usuarios van en `extensions/<slug>/template/docs/` (por ejemplo `GITHUB_SETUP_GUIDE.md`).

### Semántica de overlay `.append`

Cuando el overlay incluye archivos `*.append` (por ejemplo `docs/README.md.append`, `.env.example.append`), la CLI **añade** ese contenido al archivo existente en el proyecto generado en lugar de sobrescribirlo. Prefiere `.append` para índices de docs y samples de entorno para que addons de wave-1 y de dominio no pisen el `docs/README.md` o `.env.example` base.

### `incompatibleWith`

Declara `incompatibleWith: ["otro-addon"]` en `templates.json` **solo** cuando dos addons colisionarían en las mismas rutas de overlay (por ejemplo ambos escriben `.github/workflows/ci.yml`). No inventes conflictos blandos.

## Checklist de plantilla (baseline L0)

Crea `templates/<slug>/` con:

| Archivo | Obligatorio | Notas |
|------|----------|-------|
| `v.mod` | sí | Nombre de módulo según convención |
| `main.v` o `src/` | sí | Entry compilable o root de librería |
| `*_test.v` | sí | Al menos un archivo `v test` |
| `README.md` | sí | Uso, build, instrucciones de run |
| `docs/README.md` | sí | Índice de docs |
| `docs/PROJECT_STRUCTURE.md` | sí | Layout + convenciones de features |
| `docs/TESTING.md` | sí | Cómo correr tests |

## Checklist de plantilla (M1)

Ver [TEMPLATE_QUALITY_M1.md](./TEMPLATE_QUALITY_M1.md). Resumen:

| Archivo | Notas |
|------|-------|
| `AGENTS.md`, `CONTRIBUTING.md`, `.env.example`, `QUALITY.md` | Root |
| `docs/CONFIGURATION.md`, `docs/DEPLOYMENT.md` | Todas las M1 |
| `docs/API.md` | Solo `web-server` |
| `_module_template/` + ≥1 módulo de feature | Apps / bases de dominio |

M1 se valida vía `M1_QUALITY_ALLOWLIST` en `scripts/ci/validate-registry.py`.

### Módulos de feature (V-native)

Prefiere un directorio por feature en el **root del proyecto** (`greet/`, `health/`, `checksum/`). V resuelve `import greet` a un `greet/` top-level — `src/features/<name>/` anidado no es importable sin `-path` custom.

Incluye `_module_template/` junto a features reales para que el usuario copie/pegue un nuevo módulo.

Para apps `veb`, mantén los métodos de ruta sobre `App` en `main.v` y pon helpers en un módulo de feature.

Registro en `templates.json`:

```json
{
  "name": "mi-template",
  "description": "Resumen en una línea",
  "url": "https://github.com/Create-Vlang-App/cva-templates?subdir=templates/mi-template",
  "kind": "template",
  "tags": ["wave-1"]
}
```

Validación:

```bash
python scripts/ci/validate-registry.py
cd templates/mi-template && v test .
```

## Checklist de extensión

Crea:

```text
extensions/<slug>/
├── README.md                 # docs del banco (no se fusiona)
└── template/                 # root del overlay (se fusiona)
    ├── ...                   # archivos copiados al proyecto
    └── docs/                 # guías opcionales para usuario
        ├── SOME_GUIDE.md
        └── README.md.append  # preferido para actualizar índice
```

El `README.md` del banco debe incluir una sección **Verify after scaffold** (comandos que el usuario ejecuta tras habilitar el addon).

Registro bajo `addons` en `templates.json`:

```json
{
  "name": "mi-extension",
  "description": "Qué añade",
  "url": "https://github.com/Create-Vlang-App/cva-templates?subdir=extensions/mi-extension",
  "kind": "addon",
  "tags": ["wave-1"],
  "compatibleWith": ["web-server", "cli-app"]
}
```

### Addons de dominio

Prefiere **módulos con nombre** bajo el overlay (por ejemplo `template/plotting/`) en lugar de `template/src/*.v` planos con `module main`, para que los merges no colisionen entre addons. Ver [DOMAIN_AUTHORING.md](./DOMAIN_AUTHORING.md).

## Reglas de nombres

- Slugs: minúsculas, separados por guión (`web-server`, `v-docker`).
- El nombre del directorio debe coincidir con el segmento `subdir` en la URL.
- **No renombres slugs existentes** sin nota de migración en [`docs/MAINTENANCE_TEMPLATES.md`](./MAINTENANCE_TEMPLATES.md).
- Convenciones solo para extensiones **nuevas**:
  - `all-*` — transversal (cualquier base) — en CVA se usa sin prefijo `all-` por legacy (`github-setup`, `development-container`)
  - `web-*` — orientado a web-server
  - `vsl-*` / `vtl-*` / `rxv-*` — alcance de dominio

Los slugs wave-1 existentes (`github-setup`, `v-docker`, `v-fmt-vet`, …) se mantienen tal cual.

## Ejemplo: plantilla CLI mínima

```text
templates/cli-app/
├── v.mod
├── main.v
├── main_test.v
├── greet/
│   ├── greet.v
│   └── greet_test.v
├── _module_template/
│   ├── module.v
│   └── module_test.v
├── README.md
├── AGENTS.md
├── CONTRIBUTING.md
├── .env.example
├── QUALITY.md
└── docs/
    ├── README.md
    ├── PROJECT_STRUCTURE.md
    ├── TESTING.md
    ├── CONFIGURATION.md
    └── DEPLOYMENT.md
```

## Ejemplo: extensión github-setup

```text
extensions/github-setup/
├── README.md
└── template/
    ├── .github/workflows/ci.yml
    └── docs/
        ├── GITHUB_SETUP_GUIDE.md
        └── README.md.append
```

El workflow debe usar [`vlang/setup-v`](https://github.com/vlang/setup-v) con inputs `version-file` o `stable`.

## Perfiles CI (L3)

Añade `ci/profiles/<id>.json`:

```json
{
  "id": "web-server-github",
  "description": "Web server con GitHub CI",
  "templateDir": "web-server",
  "addons": ["github-setup"]
}
```

Ejecuta `python scripts/ci/generate-matrix.py --layer validate-profiles` antes de pushear.

## Barra de revisión

- Compila con `v` en Linux (canónico en CI)
- Tests pasan (`v test`)
- Registro valida (L0) — incluye checks de docs + `template/` (+ M1 para templates en allowlist)
- Scaffold check pasa cuando la CLI está disponible (L1+)

Ver [ARCHITECTURE.md](ARCHITECTURE.md) para convenciones de merge y URLs.

## Catálogo de dominio (científico / ML / reactivo)

Ver [DOMAIN_AUTHORING.md](./DOMAIN_AUTHORING.md) y [recipes/DOMAIN_RECIPES.md](./recipes/DOMAIN_RECIPES.md). Las bases están bloqueadas en 3 (`vsl-starter`, `vtl-starter`, `rxv-starter`); nuevas capacidades se añaden como addons.

## Pruebas locales

Apunta la CLI a un checkout local:

```bash
create-vlang-app ./mi-app \
  --template web-server \
  --addons github-setup \
  --catalog-path templates.json \
  --no-interactive --force --no-install

cd mi-app
v test .
v fmt -w .
v vet .
```

También ejecuta cualquier verificación específica documentada en el README de cada extensión.

## Checklist para nuevas plantillas

* `v.mod` con metadata válida.
* Arquitectura de features/módulos (no un ejemplo plano "hello world").
* Los archivos `docs/` requeridos según checklist M1 cuando corresponda.
* Entrada en `templates.json` con `kind` y `tags` correctos.
* `README`, `CONTRIBUTING`, `AGENTS` y docs completas en `docs/` (según barra de calidad).
* Prueba local de generación completada.

## Checklist para nuevas extensiones

* Tipos compatibles coinciden con plantillas objetivo; usa compatibilidad amplia solo cuando sea realmente portable.
* Archivos generados dentro de `template/`; el `README.md` del catálogo queda fuera y no sobrescribe el README del proyecto.
* Incluye `docs/<TOPIC>_GUIDE.md` y `docs/README.md.append` cuando añade docs al proyecto generado.
* Usa `.append` para no pisar índices o `.env.example` existentes.
* Define `compatibleWith` para bases específicas de dominio y `incompatibleWith` para extensiones mutuamente incompatibles.
* El README del catálogo explica cuándo usar la extensión, qué copia y cómo verificarla.
* Entrada en `templates.json` existe y la URL `subdir` coincide con el nombre de la carpeta.

## Futuras plantillas

Las plantillas planificadas aún no registradas se discuten en issues del repo. Ver [MAINTENANCE_TEMPLATES.md](./MAINTENANCE_TEMPLATES.md).

## Catálogo AI/ML

Para taxonomía AI/ML, categorías y reglas entre plantillas y extensiones consulta [DOMAIN_AUTHORING.md](./DOMAIN_AUTHORING.md).

---

> **Nota:** La versión canónica es `AUTHORING.md` en inglés. Esta traducción mantiene los términos técnicos (`template`, `addon`, `slug`, `compatibleWith`, `v.mod`, `v test`) en inglés para consistencia con la CLI y el código.
