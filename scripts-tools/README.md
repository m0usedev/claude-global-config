# Introducion

La finalidad de los **scripts-tools** es el poder hacer acciones referentes a claude que con promts no se pueden o sobre configuraciones rapidas.

# Instalacion

1. Instala python en tu sistema.

2. Crea un entorno virtual en tu `scripts-tools` con `python3 -m venv venv`.

3. Activa el entorno virtual `source ./venv/bin/activate`.

4. Instala las dependencias `pip install -r requirements.txt`

  - Si haces tus modificaciones y necesitas referscar la lista de dependencis usa `pip freeze > requirements.txt`

5. Ahora necesitamos darle a los scripts permisos de ejecucion con `chmod +x ~/.claude/scripts-tools/*.py`

6. Agrega el siguiente path a tu `~/.bashrc` o `~/.zshrc`.
  ```bash
  export PATH="$HOME/.claude/scripts-tools:$PATH"
  ```

7. Recarga la configuracion con `source ~/.bashrc` o `source ~/.zshrc`.

8. Ya puedes disfrutar de tus comandos.

9. Prueba `hello_world.py`.