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

# Recomendaciones de uso

## Hablar en ingles

Los sistemas de tokenizacion de los textos que le mandamos la ia (tokenizer) esta entrenado sobre todo en ingles, lo que hace que sea mucho mas eficiente y barato tokenizar un texto en ingles que en español o chino.

Recomendaciones para mejorar el ingles y practicar este proceso:

1. Un corrector de ortografia de ingles antes de mandar los mensaje [zerogpt | grammar-checker](https://www.zerogpt.com/grammar-checker)
2. Usar el traductor de google para encontrar las palabras que te faltan o ver si lo que pusiste tiene sentido [google translate](https://translate.google.com/?hl=es&sl=en&tl=es&op=translate)

## Tareas concisas, marcadas y acotadas

Cuando una tarea crece, tanto en numero de mensajes en la conversaicon como en el tamaño de la respuesta / actiones que tiene que realizar claude, la efectividad y la claridad de lo que tieen que hacer se diluye.

En el caso de una **conversacion larga** claude tienede a tener mas en cuenta los primeros y ultimo mensaje, haciendo que se diluya lo del medio, sin mencionar el tamaño que ya este ocupando la conversacion en el contexto, empezando a decrecer la eficacia a partir del 50%.

**Este mismo efecto de diluido sucede con textos que le mandes que sea muy largos** y o que impliquen mucha cantidad de informacion que el tenaga que revisar del proyecto para llevar acabo la tarea, como por ejemplo un refactor que implique leer 50 mil lineas de codigo. Lo mas apropiado para tener un buen control de lo que hacemos es usarle en casos donde le decimos y tenemos conocimientos de la gran mayoria de la tarea que queremos que haga, asi le dejaremos marcado todo el camino que tiene que hacer. No queremos invertir una hora haciendola, es mas facil 10 minutos en un buen pront para que la haga el.

En el caso del **tamaño de una respuesta** si esta es muy larga y tiene que hacer muchas actiones tambien es posible que alucine y haga cosas que no estaban planeadas en un principio. Siguiendo con el ejemplo del refactor anterior que toque funciones que le dijiste que no tocase o que no tendria que haber tocado para lo que tenia que hacer.

En conclusion:

1. Un chat tiene que ser sobre una tarea especifica, no mas.
2. Se claro y conciso en lo que tiene que realizar.
3. Que la ejecucion que tiene que realizar siga la misma filosofia de simpleza y concision para tener un mayor control y eficiencia.

# statusbar

Tenego una statusbar personalizada `statusline.sh` que muestra el modelo que se esta usando, si tienel thinking mode activado, el contexto usado en el chat, los tokens usados y cuanto falta para que se reseteen.

Esto esta configurado tambien en los settings.json

```json
"statusLine": {
  "type": "command",
  "command": "~/.claude/statusline.sh"
}
```

Apareciendo algo como.

```
[Sonnet] | 🧠 ON | 📊 ctx: 34% | 🎯 tokens: 58% | ⏳ reset en: 2h 30m
```

En caso de que no funcione prueba prineor a daler al archivo permisos de ejecucion con `chmod +x ~/.claude/statusline.sh`.

Mas info sobre la personalizacion en [statusline](https://code.claude.com/docs/en/statusline).

---

# comandos para ocnfigurar el modelo

```bash
alias claude-super-easy='MAX_THINKING_TOKENS=0 claude --permission-mode auto --model sonnet --effort medium'
alias claude-easy='MAX_THINKING_TOKENS=0 claude --permission-mode plan --model sonnet --effort high'
alias claude-normal='claude --permission-mode plan --model opus --effort medium'
alias claude-hard='claude --permission-mode plan --model opus --effort high'
```

```bash
MAX_THINKING_TOKENS=0 claude --permission-mode auto --model sonnet --effort medium
MAX_THINKING_TOKENS=0 claude --permission-mode plan --model sonnet --effort high
claude --permission-mode plan --model opus --effort medium
claude --permission-mode plan --model opus --effort high
```

# cosas que meter en el claude.md

- mirar una forma de que me recuerde que use el ingles antes de seguir tokenizando alguna conversacion.
- que las respuestas que me de sean en ingles.
- que me de una alerta si alguna habilidad o configuracion la tengo en otro idioma que no sea ingles

- ver como manipular el modo thinking

- poder ver en los datos debajo del chat: modelo, thinming on / off, porcentaje contexto (alerta al 50%), uso de tokens, tiempo faltante para el reset de los tokens

- es muchisimo mas importante el primer pront que los siguientes (ver el dale las skils y datos necesraios para el contexto de latarea antes de empezarla)