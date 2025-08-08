.data
    a: .word 10
    b: .word 5
    resultado: .word 0
    str_0: .ascii "Iniciando programa\n"
    len_str_0 = . - str_0
    str_1: .ascii "Suma completada\n"
    len_str_1 = . - str_1
    str_2: .ascii "a es menor que b\n"
    len_str_2 = . - str_2
    str_3: .ascii "a es mayor que b\n"
    len_str_3 = . - str_3
    str_4: .ascii "Multiplicacion completada\n"
    len_str_4 = . - str_4
    str_5: .ascii "Resta completada\n"
    len_str_5 = . - str_5

.text
.global _start
_start:
    @ Imprimir string: Iniciando programa
    MOV R7, #4        @ syscall write
    MOV R0, #1        @ stdout
    LDR R1, =str_0 @ dirección del string
    MOV R2, #len_str_0 @ longitud del string
    SWI 0             @ llamada al sistema
    @ Suma: resultado = a + b
    LDR R0, =a   @ Cargar dirección de a
    LDR R0, [R0]      @ Cargar valor de a
    LDR R1, =b  @ Cargar dirección de b
    LDR R1, [R1]      @ Cargar valor de b
    ADD R2, R0, R1    @ R2 = R0 + R1
    LDR R3, =resultado @ Dirección de resultado
    STR R2, [R3]      @ Guardar resultado en resultado
    @ Imprimir string: Suma completada
    MOV R7, #4        @ syscall write
    MOV R0, #1        @ stdout
    LDR R1, =str_1 @ dirección del string
    MOV R2, #len_str_1 @ longitud del string
    SWI 0             @ llamada al sistema
    @ if a < b
    LDR R0, =a   @ Cargar dirección de a
    LDR R0, [R0]      @ Cargar valor de a
    LDR R1, =b  @ Cargar dirección de b
    LDR R1, [R1]      @ Cargar valor de b
    CMP R0, R1        @ Comparar R0 y R1
    BGE L1  @ Branch if Greater or Equal (negación de <)
    @ Imprimir string: a es menor que b
    MOV R7, #4        @ syscall write
    MOV R0, #1        @ stdout
    LDR R1, =str_2 @ dirección del string
    MOV R2, #len_str_2 @ longitud del string
    SWI 0             @ llamada al sistema
    B L0     @ Saltar al final
L1:
    @ else (vacío)
L0:
    @ if a > b
    LDR R0, =a   @ Cargar dirección de a
    LDR R0, [R0]      @ Cargar valor de a
    LDR R1, =b  @ Cargar dirección de b
    LDR R1, [R1]      @ Cargar valor de b
    CMP R0, R1        @ Comparar R0 y R1
    BLE L3  @ Branch if Less or Equal (negación de >)
    @ Imprimir string: a es mayor que b
    MOV R7, #4        @ syscall write
    MOV R0, #1        @ stdout
    LDR R1, =str_3 @ dirección del string
    MOV R2, #len_str_3 @ longitud del string
    SWI 0             @ llamada al sistema
    B L2     @ Saltar al final
L3:
    @ else (vacío)
L2:
    @ Multiplicacion: resultado = a * b
    LDR R0, =a   @ Cargar dirección de a
    LDR R0, [R0]      @ Cargar valor de a
    LDR R1, =b  @ Cargar dirección de b
    LDR R1, [R1]      @ Cargar valor de b
    MUL R2, R0, R1    @ R2 = R0 * R1
    LDR R3, =resultado @ Dirección de resultado
    STR R2, [R3]      @ Guardar resultado en resultado
    @ Imprimir string: Multiplicacion completada
    MOV R7, #4        @ syscall write
    MOV R0, #1        @ stdout
    LDR R1, =str_4 @ dirección del string
    MOV R2, #len_str_4 @ longitud del string
    SWI 0             @ llamada al sistema
    @ Resta: resultado = a - b
    LDR R0, =a   @ Cargar dirección de a
    LDR R0, [R0]      @ Cargar valor de a
    LDR R1, =b  @ Cargar dirección de b
    LDR R1, [R1]      @ Cargar valor de b
    SUB R2, R0, R1    @ R2 = R0 - R1
    LDR R3, =resultado @ Dirección de resultado
    STR R2, [R3]      @ Guardar resultado en resultado
    @ Imprimir string: Resta completada
    MOV R7, #4        @ syscall write
    MOV R0, #1        @ stdout
    LDR R1, =str_5 @ dirección del string
    MOV R2, #len_str_5 @ longitud del string
    SWI 0             @ llamada al sistema
    @ Terminar programa
    MOV R7, #1       @ syscall exit
    MOV R0, #0       @ código de salida
    SWI 0            @ llamada al sistema