# Ingeniería de prompts

## Ejercicio 1: Generar un cartel para un curso. 

### Instrucciones: 

Genera una imagen publicitaria vertical, proporción 4:5, para promover el curso hipotético “Python para análisis de datos” entre principiantes.

Muestra un escritorio contemporáneo con una computadora portátil y una libreta. La pantalla presenta visualizaciones abstractas y formas de código sin texto legible. Estilo de fotografía editorial realista, ambiente profesional y accesible, iluminación lateral suave.

Composición: coloca la computadora en la mitad inferior derecha. Reserva aproximadamente el 30% superior y una franja inferior despejados para añadir titular y marca después.

Usa fondo negro #090909, superficies grafito #1B1B1B, acentos naranja #F04A1D y pequeños detalles blancos. Los colores son una referencia visual; el acabado final se ajustará en el editor.

Entrega una imagen. No incluyas letras, logotipos, marcas de agua, precios, fechas ni insignias. El logo EDL se colocará después desde su archivo original, sin regenerarlo.

### Corrección:

Edita la imagen anterior. Conserva la composición, los objetos, la paleta y las áreas libres.

Crea una segunda variante cambiando únicamente la iluminación: utiliza luz frontal suave, con menor contraste sobre la computadora. Mantén el fondo oscuro y evita introducir texto o logos.

Entrega la variante por separado para compararla con la original.


## Ejercicio 2: Caja registradora con Python (pendiente para la siguiente clase)

### Instrucciones: 

Desarrolla una caja registradora de consola para principiantes, compatible con Python 3.12 o posterior y usando solo biblioteca estándar. Trabaja en español y en MXN.

Catálogo fijo: C01 = Cuaderno a 25.50; P01 = Pluma a 10.00; B01 = Borrador a 7.25. Los precios son finales: no agregues impuestos. Permite agregar códigos y cantidades enteras positivas, acumular productos repetidos, ver carrito, cobrar o cancelar.

Al cobrar, solicita un descuento porcentual entre 0 y 100 y un pago en efectivo igual o mayor al total. Rechaza una venta vacía. Usa Decimal construido desde cadenas; rechaza valores no finitos, negativos o mal formados. Redondea el descuento a 0.01 con ROUND_HALF_UP, calcula total = subtotal - descuento y cambio = pago - total.

Separa las funciones de cálculo de la interacción input/print. El ticket debe mostrar productos, cantidades, precios unitarios, importes, subtotal, descuento, total, pago y cambio con dos decimales.

Entrega caja_registradora.py, test_caja.py con unittest y un README con comandos de ejecución. Antes de escribir el código, resume el flujo y las funciones en ocho líneas como máximo. Si puedes ejecutar, corre las pruebas y reporta sus resultados; si no puedes, indica que están pendientes de ejecución.



