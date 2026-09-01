# Introducion

La finalidad de los **scripts-tools** es el poder hacer acciones referentes a claude que con promts no se pueden o sobre configuraciones rapidas.

# Instalacion

1. Instala python en tu sistema.

2. Crea un entorno virtual en tu `scripts-tools` con `python3 -m venv venv`.

3. Activa el entorno virtual `source ./venv/bin/activate`.

4. Instala las dependencias `pip install -r requirements.txt`

  - Si haces tus modificaciones y necesitas referscar la lista de dependencis usa `pip freeze > requirements.txt`

5. Los scripts reales viven en `~/.claude/scripts-tools/tools`. Ejecuta el instalador para crear enlaces simbolicos hacia ellos en `~/.local/bin` (que ya deberia estar en tu `PATH`):
  ```bash
  python3 ~/.claude/scripts-tools/install.py
  ```
  Esto le da permisos de ejecucion a cada script de `tools/` y crea un symlink por script (sin la extension `.py`) en `~/.local/bin`.

6. Ya puedes disfrutar de tus comandos.

7. Prueba `hello_world`.

## Desinstalar

Para quitar los enlaces simbolicos creados por `install.py`:
```bash
python3 ~/.claude/scripts-tools/uninstall.py
```
Esto solo elimina los symlinks en `~/.local/bin` que apuntan a `~/.claude/scripts-tools/tools`; no toca los scripts originales.