.text
.global _start

_start:
    @ Cargar valores en registros
    MOV R0, #10       @ Primer número
    MOV R1, #5        @ Segundo número

    @ Sumar R0 + R1 -> R2
    ADD R2, R0, R1    @ R2 = 10 + 5 = 15

    @ Restar R0 - R1 -> R3
    SUB R3, R0, R1    @ R3 = 10 - 5 = 5

    @ Comparar R2 y R3
    CMP R2, R3        @ Compara si R2 > R3, R2 < R3, R2 == R3

    @ Condicional: si R2 > R3, saltar a etiqueta mayor
    BGT mayor         @ Branch if Greater Than
    BLT menor         @ Branch if Less Than
    BEQ iguales       @ Branch if Equal

mayor:
    @ Si R2 > R3, poner 1 en R4
    MOV R4, #1
    B fin

menor:
    @ Si R2 < R3, poner 2 en R4
    MOV R4, #2
    B fin

iguales:
    @ Si son iguales, poner 3 en R4
    MOV R4, #3

fin:
    @ Terminar programa (salir)
    MOV R7, #1       @ syscall número para exit
    MOV R0, R4       @ código de salida en R0
    SWI 0            @ llamada al sistema