## Automatización de facturas y boletas PDF a Excel

¿Tu equipo copia manualmente información de facturas o boletas a una planilla? Este proyecto busca simplificar esa tarea mediante un script en Python que extrae campos reconocibles de documentos PDF y genera resultados organizados en Excel.

### ¿Qué hace?

- Busca datos como empresa o proveedor, fecha y monto total mediante patrones de extracción.
- Organiza los resultados en una planilla Excel.
- Genera un informe para revisar los documentos procesados.
- Permite identificar casos que requieren revisión manual.

### Formatos compatibles

**Probado:** dos formatos distintos de documentos —facturas y boletas—, con 4 de 4 documentos procesados correctamente en la muestra de prueba.

**Limitaciones actuales:**
- Necesita PDF con texto seleccionable; no procesa directamente documentos escaneados como imágenes.
- Los campos deben contener etiquetas o patrones que el extractor pueda reconocer.
- Los formatos completamente distintos pueden requerir ajustes en los patrones de extracción.
- Los resultados deben revisarse antes de utilizarlos en procesos contables.

La prueba de 4 documentos es una validación inicial, no una garantía de precisión para cualquier documento.

### Servicio piloto para pymes

Estoy buscando empresas y oficinas contables interesadas en evaluar esta automatización con una muestra pequeña de documentos compatibles.

El piloto permite comprobar qué campos se extraen correctamente, identificar excepciones y estimar si el flujo puede reducir trabajo manual.

La compatibilidad se revisa antes de acordar el alcance. Los documentos del cliente se tratarán con autorización y confidencialidad; no se publicarán en este repositorio.

### ¿Quieres evaluar tu proceso?

Repositorio y demostración técnica:  
https://github.com/AbrihamTek/automatizacion-documentos

Para evaluar una posible colaboración, contacta al desarrollador y coordinemos una demostración breve con datos ficticios o anonimizados.