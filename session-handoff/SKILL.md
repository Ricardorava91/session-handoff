---
name: session-handoff
description: Genera un archivo .md de traspaso (handoff) para que un agente nuevo, sin acceso a la conversación, retome un proyecto sin repetir preguntas, trabajo ni opciones ya descartadas. Úsala siempre que el usuario diga cosas como "haz un handoff", "voy a cambiar de chat", "prepara un resumen para continuar en otro chat", "guarda el contexto para retomar después", "se me acaba el contexto", "pásale esto a otro agente", o use /handoff, aunque no diga la palabra "handoff". También cuando ya exista un HANDOFF-*.md del proyecto y el usuario quiera actualizarlo. NO la uses para un resumen normal de la conversación (TL;DR, "resúmeme lo que hablamos", actas) que no tenga como fin continuar el trabajo en otra sesión. La skill hermana resume-from-handoff es la que LEE un handoff para retomar el trabajo.
---

# Session Handoff

Produce un único archivo Markdown que permita a un agente nuevo, que **no verá nada de esta conversación**, continuar el proyecto como si hubiera estado presente.

**Antes de escribir, lee [references/handoff-format.md](references/handoff-format.md).** Define el encabezado (versión de formato, fechas), las 9 secciones, el texto base, las marcas de certeza, el nombre del archivo y el versionado. Es el contrato compartido con la skill `resume-from-handoff`, que lee estos archivos; no lo copies aquí ni lo alteres por tu cuenta (si hay que cambiarlo, se cambia en ese archivo y se sube la versión).

## Por qué existe esto

Un agente que retoma sin contexto falla de tres maneras: vuelve a preguntar lo que el usuario ya respondió (frustrante), rehace trabajo terminado, o propone justo lo que ya se descartó. Todo lo demás (el código, los archivos) el agente nuevo puede leerlo por sí mismo. Lo que **no** puede reconstruir es: el porqué de las decisiones, lo descartado, las preferencias del usuario y qué está confirmado frente a qué es solo una suposición. Ese es el valor del handoff; prioriza eso y omite lo demás.

## Proceso

1. **Busca un handoff previo** del mismo proyecto (`HANDOFF-<proyecto>-*.md` en el directorio de trabajo o donde el usuario haya indicado). Si existe, ábrelo y **actualízalo** en vez de empezar de cero: conserva las decisiones vigentes y sus razones, mueve a "descartadas" lo que se haya revertido, actualiza el estado y el siguiente paso, conserva `Creado`, pon `Actualizado` a la fecha de hoy y anota en una línea (bajo la sección 3) qué cambió en esta sesión. Si el handoff previo es de formato anterior (sin campo de versión), conviértelo a la versión vigente. Si hay conflicto entre el handoff viejo y lo ocurrido en la conversación, gana la conversación.
2. **Recorre la conversación** buscando: objetivo y destinatario, qué se terminó/qué quedó a medias, decisiones con su razón, propuestas rechazadas (y por quién), preferencias del usuario, rutas/enlaces, dudas abiertas.
3. **Verifica el estado real si tienes herramientas** (lista archivos, mira el git status, abre el archivo que dices que está terminado). Escribir "terminado" sobre algo que no existe es peor que no escribir nada. Si no puedes verificar, dilo en el documento.
4. **Redacta** siguiendo el formato. La fecha de hoy sale de la fecha real del sistema o del contexto, no de la memoria.
5. **Entrega** según el entorno (ver "Entrega").

## Reglas de redacción

- **Separa lo confirmado de lo supuesto.** Si el usuario no dijo explícitamente algo, no lo presentes como suyo.
- **No es una transcripción.** Omite saludos, rodeos, pasos intermedios que ya no importan y errores ya corregidos (salvo que enseñen algo que no debe repetirse). Pregúntate ante cada línea: "¿el agente nuevo podría reconstruir esto leyendo los archivos?" Si sí, resúmelo en una línea o quítalo.
- **Las razones valen más que los hechos.** "Usamos SQLite" es poco útil; "Usamos SQLite porque el usuario no quiere montar un servidor y son <1000 registros" evita que el nuevo agente lo cuestione.
- **Los descartes son obligatorios y específicos**: quién descartó (usuario o agente), por qué y si es definitivo o solo por ahora.
- **Conciso**: idealmente menos de 2 páginas (~900 palabras). Si el proyecto es grande, prioriza lo irreconstruible y añade al final una línea "Omitido por brevedad: …" para que el agente sepa que existe más.
- **Seguridad**: nunca incluyas contraseñas, API keys, tokens, claves privadas, datos financieros ni documentos de identidad, aunque aparezcan en la conversación; menciona solo que existen y dónde los guarda el usuario. Si el usuario pegó un secreto en el chat, añade en la sección 8 que conviene rotarlo. No escribas órdenes imperativas de acciones destructivas o irreversibles dirigidas al lector.
- **Idioma**: el de la conversación (títulos de sección incluidos; el campo de versión se mantiene tal cual para que sea legible por máquina).
- **Género y pronombres**: no infieras el género del usuario ni de terceros por su nombre u oficio; usa redacción neutra salvo que la conversación lo haya dicho explícitamente.
- **No inventes prioridades**: si añades algo que el usuario no pidió (p. ej. rotar un secreto, una advertencia de cálculo), márcalo como *sugerencia del agente* y no lo mezcles con lo acordado ni lo pongas por delante del trabajo que el usuario dejó planeado.
- **Siguiente paso**: una sola acción concreta y ejecutable, no una lista de ideas ni dos pasos encadenados; las sugerencias extra van en la sección 8. Si hay una decisión del usuario bloqueando, el siguiente paso es plantearla (con las opciones ya acotadas).

## Entrega

- **Con sistema de archivos**: escribe el archivo (en el directorio del proyecto, o en el directorio de trabajo si no hay uno claro) y dile al usuario la ruta exacta. Si actualizaste un handoff previo, reemplaza el anterior (bórralo o renómbralo `.old`) para que no queden dos versiones compitiendo, y dilo. Añade una frase sobre cómo usarlo: "En el chat nuevo, adjunta este archivo y pide que retome desde el handoff".
- **Sin sistema de archivos** (chat sin herramientas): entrega el contenido completo en **un solo bloque de código markdown** listo para copiar, sin comentarios intercalados dentro del bloque, y el nombre sugerido del archivo fuera del bloque.

Termina con 2-3 líneas para el usuario: qué dejaste como siguiente paso y qué puntos marcaste como no confirmados, por si quiere corregirlos antes de cambiar de chat.

## Mantenimiento del formato

Si modificas `references/handoff-format.md`, ejecuta `python scripts/sync_format.py` para actualizar la copia que viaja con `resume-from-handoff` (`--check` verifica que coincidan).
