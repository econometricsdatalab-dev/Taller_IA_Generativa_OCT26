# Prompts vistos en sesión

## P1 · Caja registradora · prompt completo

```text
Desarrolla una caja registradora de consola para principiantes, compatible con Python 3.12 o posterior y usando solo biblioteca estándar. Trabaja en español y en MXN.

Catálogo fijo: C01 = Cuaderno a 25.50; P01 = Pluma a 10.00; B01 = Borrador a 7.25. Los precios son finales: no agregues impuestos. Permite agregar códigos y cantidades enteras positivas, acumular productos repetidos, ver carrito, cobrar o cancelar.

Al cobrar, solicita un descuento porcentual entre 0 y 100 y un pago en efectivo igual o mayor al total. Rechaza una venta vacía. Usa Decimal construido desde cadenas; rechaza valores no finitos, negativos o mal formados. Redondea el descuento a 0.01 con ROUND_HALF_UP, calcula total = subtotal - descuento y cambio = pago - total.

Separa las funciones de cálculo de la interacción input/print. El ticket debe mostrar productos, cantidades, precios unitarios, importes, subtotal, descuento, total, pago y cambio con dos decimales.

Entrega caja_registradora.py, test_caja.py con unittest y un README con comandos de ejecución. Antes de escribir el código, resume el flujo y las funciones en ocho líneas como máximo. Si puedes ejecutar, corre las pruebas y reporta sus resultados; si no puedes, indica que están pendientes de ejecución.
```

## Prompt de depuración con evidencia

```text
Al ejecutar caja_registradora.py ocurrió el siguiente problema.

ENTORNO: [sistema y versión de Python].
ENTRADAS: [secuencia exacta introducida].
ESPERADO: [resultado].
OBSERVADO: [salida o traceback completo].
CÓDIGO: [adjunta la versión que ejecutaste].

Identifica la causa apoyándote en esta evidencia. Corrige el defecto conservando las reglas del ejercicio. Agrega una prueba que reproduzca el fallo y vuelve a ejecutar las pruebas afectadas. Distingue las pruebas ejecutadas de las que propones.
```

## W1 · Informe Word · prompt completo

```text
Crea una base editable de informe técnico de análisis de datos con identidad visual EDL. Adjunto logo_EDL_oficial.png. Conserva exactamente su forma, colores y proporción; colócalo sobre una banda negra #090909.

Formato: A4 vertical; márgenes 2.5 cm; interior blanco; texto #222222; acento #F04A1D. Arial 11 pt, interlineado 1.15 y 6 pt después de párrafo. Usa estilos reales Normal, Título 1, Título 2, Leyenda y Tabla, con jerarquía uniforme.

Incluye portada con [TÍTULO], [SUBTÍTULO], [AUTOR], [FECHA] y [VERSIÓN]. Después, ocho secciones: Resumen ejecutivo, Objetivos, Datos y fuentes, Metodología, Resultados, Limitaciones, Conclusiones y Referencias. Añade encabezado y numeración de página automática en el cuerpo; la portada no debe mostrar número.

Incluye una tabla editable de cuatro columnas: Indicador, Valor, Unidad y Fuente. Añade dos espacios para figuras con sus leyendas y campos [FUENTE], [PERIODO] y [RESULTADO]. Deja campos explicativos en lugar de inventar estadísticas o bibliografía.

Si tienes herramientas para crear archivos, entrega Base_Informe_EDL.docx. Si no, entrega un script completo con python-docx y pasos para ejecutarlo usando el logo adjunto. Explica cómo guardarlo como plantilla .dotx desde Word; no cambies únicamente la extensión.

Antes de entregar, comprueba estilos, salto después de portada, continuidad de numeración, tabla editable y ausencia de recortes. Indica qué verificaste realmente y qué revisión queda pendiente en Word.
```

## Iteración: comprobar que la plantilla soporta contenido

```text
Usa una copia de la base de informe anterior. Añade texto ilustrativo claramente marcado hasta ocupar al menos cuatro páginas de cuerpo, amplía la tabla a 15 filas e inserta una figura de muestra.

Verifica encabezados, numeración, cortes de tablas, títulos sin párrafos huérfanos y tamaño del logo. Si detectas un defecto, corrígelo en estilos o configuración de página.

Conserva la plantilla limpia por separado. Entrega la copia de prueba y describe los ajustes realizados; no presentes contenido ilustrativo como resultados de investigación.
```
