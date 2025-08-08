Generador de Código Ensamblador
Este proyecto implementa un sistema que genera código ensamblador ARM a partir de un lenguaje de alto nivel simplificado. Incluye un analizador léxico, un analizador sintáctico y un generador de código que convierte instrucciones en ensamblador ARM ejecutable.
Estructura del Proyecto

sample.s: Ejemplo de código ensamblador ARM que realiza operaciones aritméticas (suma, resta), comparaciones y saltos condicionales. Sirve como referencia para entender la salida esperada del generador.
lexer.py: Implementa el analizador léxico (Lexer) que convierte el código fuente en una secuencia de tokens, identificando palabras reservadas, operadores, números y cadenas.
parser.py: Contiene el analizador sintáctico (SyntacticAnalyzer) que procesa los tokens y genera un árbol sintáctico abstracto (AST) basado en una gramática definida para frases y estructuras condicionales.
code_generator.py: Implementa el generador de código (AsmGenerator) que transforma el AST en código ensamblador ARM. También incluye una función para generar ejemplos de código ensamblador (generar_ejemplo) y un programa principal para probar el sistema.

Requisitos

Python 3.x
No se requieren dependencias externas adicionales.

Instalación

Clona o descarga este repositorio.
Asegúrate de tener Python 3.x instalado en tu sistema.
Coloca todos los archivos (sample.s, lexer.py, parser.py, code_generator.py) en el mismo directorio.

Uso

Ejecuta el script principal code_generator.py:
python code_generator.py


El programa procesará un código fuente de ejemplo definido en code_generator.py y generará:

Archivos sample1.s, sample2.s, sample3.s con ejemplos de ensamblador ARM para diferentes casos.
Un archivo ejemplo_generado.s con el código ensamblador generado a partir del código fuente de alto nivel.


El programa imprimirá el código ensamblador generado y el tiempo de ejecución.


Ejemplo de Código Fuente
El código fuente de alto nivel procesado por el programa es:
resultado = a + b
if a<b (print("a es menor que b"))
if a>b (print("a es mayor que b"))
resultado = a * b
resultado = a - b

Salida

Archivos generados (sample1.s, sample2.s, sample3.s, ejemplo_generado.s).
Mensaje de éxito en la consola con el código ensamblador generado.
Tiempo de ejecución en milisegundos.

Estructura del Código Ensamblador Generado
El código ensamblador generado sigue la arquitectura ARM e incluye:

Segmento .data: Define variables y cadenas de texto.
Segmento .text: Contiene el código ejecutable, incluyendo la función _start como punto de entrada.
Llamadas al sistema (SWI 0) para imprimir mensajes y terminar el programa.
Instrucciones para operaciones aritméticas (ADD, SUB, MUL) y comparaciones (CMP, BGT, BLT, BEQ).

Limitaciones

El analizador léxico y sintáctico está diseñado para un subconjunto limitado de un lenguaje de alto nivel (asignaciones, condicionales if, y sentencias print).
Solo soporta un conjunto predefinido de palabras (artículos, adjetivos, sustantivos, verbos, preposiciones).
La generación de código está optimizada para la arquitectura ARM.

Contribuciones
Si deseas contribuir, puedes:

Agregar soporte para más construcciones del lenguaje (e.g., bucles).
Mejorar la gramática para permitir estructuras más complejas.
Optimizar el código ensamblador generado.

Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles (si se incluye).
