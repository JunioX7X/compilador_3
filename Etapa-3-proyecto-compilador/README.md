# Compilador para Little English y Operaciones Aritméticas

## Descripción
Este proyecto es un compilador desarrollado como parte de la asignación académica para el curso de Paradigmas de Programación en **Lead University**. El compilador procesa un lenguaje que combina oraciones simples en inglés ("Little English") y operaciones aritméticas con sentencias condicionales (`if`). El programa realiza análisis léxico, sintáctico y generación de código ensamblador ARM para tres casos de prueba (`sample1.s`, `sample2.s`, `sample3.s`) y un programa generado (`ejemplo_generado.s`).

**Autor**: Jason Barrantes  
**Universidad**: Lead University  
**Curso**: Paradigmas de Programación  
**Fecha de Entrega**: 6 de agosto de 2025

## Estructura del Proyecto
El proyecto consta de los siguientes archivos principales:
- **lexer.py**: Realiza el análisis léxico, tokenizando la entrada en categorías como `IDENTIFIER`, `STRING`, `PLUS`, `IF`, etc.
- **parser.py**: Ejecuta el análisis sintáctico, construyendo un árbol de sintaxis abstracta (AST) para oraciones, asignaciones y sentencias `if`.
- **code_generator.py**: Genera código ensamblador ARM basado en el AST, produciendo los archivos `sample1.s`, `sample2.s`, `sample3.s` y `ejemplo_generado.s`.
- **sample1.s**, **sample2.s**, **sample3.s**: Archivos ensamblador con casos de prueba predefinidos (suma, resta y comparación de valores).
- **ejemplo_generado.s**: Archivo ensamblador generado a partir del programa de entrada definido en `code_generator.py`.

## Requisitos
- Python 3.x
- Un entorno virtual (recomendado, como se muestra en el uso del script).
- Opcional: Un emulador ARM (como QEMU) o hardware ARM (como Raspberry Pi) para ejecutar el código ensamblador generado.

## Instalación
1. Clona o descarga el proyecto en tu máquina local.
2. Crea y activa un entorno virtual:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate


Asegúrate de que el directorio de trabajo sea C:\dev\paradigmas de progra\entrega_3_del_compilador\parte_2 (o ajusta según tu estructura).

Uso

Ejecuta el script principal code_generator.py desde la línea de comandos:C:\dev\modeladomatematico\estudiodecaso#3\.venv\Scripts\python.exe "C:\dev\paradigmas de progra\entrega_3_del_compilador\parte_2\code_generator.py"


El programa procesará el siguiente programa de entrada (definido en code_generator.py):resultado = a + b
if a<b (print("a es menor que b"))
if a>b (print("a es mayor que b"))
resultado = a * b
resultado = a - b


Salida esperada:
Tokens generados (análisis léxico).
Lista de sentencias parseadas (análisis sintáctico).
Código ensamblador generado para ejemplo_generado.s.
Archivos sample1.s, sample2.s, y sample3.s escritos en el directorio.
Mensaje "Código generado exitosamente" y el contenido de ejemplo_generado.s.



Ejemplo de Salida
La ejecución genera:

Archivos: sample1.s, sample2.s, sample3.s, ejemplo_generado.s.
Contenido de ejemplo_generado.s (ejemplo):.data
    a: .word 10
    b: .word 5
    resultado: .word 0
    str_0: .ascii "Iniciando programa\n"
    ...
.text
.global _start
_start:
    @ Imprimir string: Iniciando programa
    MOV R7, #4        @ syscall write
    ...


Tiempo de ejecución: ~8-150 ms, dependiendo del hardware.

Ejecución del Código Ensamblador
Para probar los archivos .s generados:

Usa un ensamblador ARM:as -o sample1.o sample1.s
ld -o sample1 sample1.o
./sample1


Esto imprimirá mensajes como "Rama mayor ejecutada" o los mensajes definidos en ejemplo_generado.s (por ejemplo, "Suma completada").

Notas

El programa soporta oraciones de "Little English" (por ejemplo, the big dog runs in the house.), asignaciones aritméticas (resultado = a + b), y sentencias condicionales (if a<b (print("mensaje"))).
Para cambiar el programa de entrada, modifica la variable input_program en code_generator.py.
Asegúrate de que el directorio tenga permisos de escritura para generar los archivos .s.

Autor

Nombre: Jason Barrantes

Universidad: Lead University

Licencia
Este proyecto es para fines académicos y no está bajo ninguna licencia específica.
