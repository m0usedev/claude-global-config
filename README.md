## 🎯 Finalidad del repositorio

Este repositorio contiene mi configuración global de Claude Code (`~/.claude`), versionada para poder:

- **Replicarla en cualquier equipo** con un simple `clone` + enlace simbólico, sin tener que reconstruir a mano comandos, agentes y skills.
- **Tener historial de cambios**: si una modificación en `settings.json` o en el `CLAUDE.md` global empeora el comportamiento, puedo ver qué cambió y revertirlo.
- **Servir de referencia a otras personas**: los comandos, agentes y skills son públicos a propósito, por si a alguien le sirven como punto de partida o quiere adaptarlos.

Lo que **no** es este repositorio: no es un backup de mi entorno. No incluye credenciales, historial de conversaciones, ni nada atado a una máquina concreta. Solo la configuración reutilizable.

### Instalación

```bash
git clone <url> ~/.claude-config
ln -s ~/.claude-config/commands ~/.claude/commands
ln -s ~/.claude-config/agents   ~/.claude/agents
# ...
cp settings.example.json ~/.claude/settings.json  # y rellenar lo propio
```

---

## 🔒 Cómo está configurado el `.gitignore`

El `.gitignore` funciona con **lista blanca**, no con lista negra. Es decir: la primera regla ignora absolutamente todo y a partir de ahí se van des-ignorando de forma explícita las rutas que sí quiero publicar.

```gitignore
*          # ignora todo
!*/        # permite descender en las carpetas
!commands/**   # y solo entonces se permite lo concreto
```

El motivo es simple: en una lista negra, cualquier archivo nuevo que Claude Code genere en el futuro (una carpeta de caché, un log, un formato que hoy no existe) entra al repo por defecto y me tengo que acordar de bloquearlo. Con lista blanca, lo nuevo queda fuera hasta que yo decida lo contrario. El fallo por omisión es no publicar, que es el lado seguro.

Al final del archivo hay además un bloque de bloqueos explícitos (`.credentials.json`, `**/.env`, `*.key`, `*.pem`) que actúa como segunda barrera dentro de las rutas ya permitidas.

### ⚠️ Antes de hacer un push desde otro equipo

En una máquina nueva la carpeta puede tener archivos que aquí no existen. Comprobar siempre, en este orden:

1. **Ver qué se va a subir realmente**, no lo que crees que se va a subir:
```bash
   git add -A && git status --short
```
   Si aparece algo que no reconoces, no lo commitees hasta saber qué es.

2. **Revisar el `settings.json`**: que no se haya colado un bloque `env` con `ANTHROPIC_API_KEY`, un `apiKeyHelper`, ni configuración de servidores MCP con tokens. Los ejemplos van en `settings.example.json` con los valores vacíos.

3. **Revisar el `CLAUDE.md` global**: es donde más fácil se acumulan rutas absolutas con el nombre de usuario, nombres de clientes, URLs internas o convenciones que no son públicas.

4. **Escanear en busca de secretos** antes de publicar:
```bash
   gitleaks detect --source . --verbose
```

5. **Si algo sensible ya está commiteado**: borrarlo en un commit posterior **no sirve**, sigue en el historial y GitHub cachea los objetos. Hay que reescribir el historial con `git filter-repo` y, sobre todo, **rotar la credencial expuesta**. Dar por comprometido cualquier token que haya llegado a un commit, aunque el push nunca se completara.
