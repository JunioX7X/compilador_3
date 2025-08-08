import sys
import time
from lexer import LexicalAnalyzer, TokenType
from parser import SyntacticAnalyzer


class AsmGenerator:
    def __init__(self):
        self._label_idx = 0
        self._str_idx = 0
        self.data_seg = []
        self.text_seg = []
        self.symbol_table = {"a": 10, "b": 5}  # Valores iniciales

    def _new_label(self):
        label = f"L{self._label_idx}"
        self._label_idx += 1
        return label

    def _new_str_label(self):
        label = f"msg_{self._str_idx}"
        self._str_idx += 1
        return label

    def _add_syscall_print(self, label, comment=None):
        if comment:
            self.text_seg.append(f"    @ Imprimir string: {comment}")
        self.text_seg.extend([
            f"    MOV R7, #4",
            f"    MOV R0, #1",
            f"    LDR R1, ={label}",
            f"    MOV R2, #len_{label}",
            f"    SWI 0"
        ])

    def generar_codigo(self, instrucciones):
        self._init_data_section()
        self._init_text_section()

        for instr in instrucciones:
            tipo = instr[0]
            if tipo == "assignment":
                self._gen_assign(instr)
            elif tipo == "if":
                self._gen_if(instr)
            elif tipo == "print":
                self._gen_print(instr)
            elif tipo == "sentence":
                self._gen_sentence(instr)

        self._gen_exit()
        return "\n".join(self.data_seg + [""] + self.text_seg)

    def _init_data_section(self):
        self.data_seg.append(".data")
        for var, val in self.symbol_table.items():
            self.data_seg.append(f"    {var}: .word {val}")
        self.data_seg.append("    resultado: .word 0")
        # Mensaje inicial
        start_msg = self._new_str_label()
        self.data_seg.append(f"    {start_msg}: .ascii \"Iniciando programa\\n\"")
        self.data_seg.append(f"    len_{start_msg} = . - {start_msg}")
        self._add_syscall_print(start_msg, "Iniciando programa")

    def _init_text_section(self):
        self.text_seg.append(".text")
        self.text_seg.append(".global _start")
        self.text_seg.append("_start:")

    def _gen_sentence(self, instr):
        _, noun_phrase, verb_phrase = instr
        _, article, adjectives, noun = noun_phrase
        frase1 = f"{article} {' '.join(adjectives)} {noun}" if adjectives else f"{article} {noun}"
        lbl1 = self._new_str_label()
        self.data_seg.append(f"    {lbl1}: .ascii \"{frase1}\\n\"")
        self.data_seg.append(f"    len_{lbl1} = . - {lbl1}")
        self._add_syscall_print(lbl1, frase1)

        if verb_phrase[1]:  # Tiene complemento
            _, verb, (_, prep, (_, art2, adj2, noun2)) = verb_phrase
            frase2 = f"{verb} {prep} {art2} {' '.join(adj2)} {noun2}" if adj2 else f"{verb} {prep} {art2} {noun2}"
            lbl2 = self._new_str_label()
            self.data_seg.append(f"    {lbl2}: .ascii \"{frase2}\\n\"")
            self.data_seg.append(f"    len_{lbl2} = . - {lbl2}")
            self._add_syscall_print(lbl2, frase2)

    def _gen_assign(self, instr):
        _, target, left, op, right = instr
        op_map = {"+": "Suma", "-": "Resta", "*": "Multiplicacion"}
        msg_lbl = self._new_str_label()
        self.data_seg.append(f"    {msg_lbl}: .ascii \"{op_map[op]} completada\\n\"")
        self.data_seg.append(f"    len_{msg_lbl} = . - {msg_lbl}")

        self.text_seg.extend([
            f"    @ {op_map[op]}: {target} = {left} {op} {right}",
            f"    LDR R0, ={left}",
            f"    LDR R0, [R0]",
            f"    LDR R1, ={right}",
            f"    LDR R1, [R1]"
        ])

        if op == "+":
            self.text_seg.append("    ADD R2, R0, R1")
        elif op == "-":
            self.text_seg.append("    SUB R2, R0, R1")
        elif op == "*":
            self.text_seg.append("    MUL R2, R0, R1")

        self.text_seg.extend([
            f"    LDR R3, ={target}",
            f"    STR R2, [R3]"
        ])
        self._add_syscall_print(msg_lbl, f"{op_map[op]} completada")

    def _gen_if(self, instr):
        _, left, comp, right, print_stmt = instr
        lbl_else = self._new_label()
        lbl_end = self._new_label()
        self.text_seg.extend([
            f"    @ if {left} {comp} {right}",
            f"    LDR R0, ={left}",
            f"    LDR R0, [R0]",
            f"    LDR R1, ={right}",
            f"    LDR R1, [R1]",
            "    CMP R0, R1"
        ])
        if comp == "<":
            self.text_seg.append(f"    BGE {lbl_else}")
        elif comp == ">":
            self.text_seg.append(f"    BLE {lbl_else}")

        self._gen_print(print_stmt)
        self.text_seg.extend([
            f"    B {lbl_end}",
            f"{lbl_else}:",
            "    @ else vacío",
            f"{lbl_end}:"
        ])

    def _gen_print(self, instr):
        _, text = instr
        lbl = self._new_str_label()
        self.data_seg.append(f"    {lbl}: .ascii \"{text}\\n\"")
        self.data_seg.append(f"    len_{lbl} = . - {lbl}")
        self._add_syscall_print(lbl, text)

    def _gen_exit(self):
        self.text_seg.extend([
            "    @ Terminar programa",
            "    MOV R7, #1",
            "    MOV R0, #0",
            "    SWI 0"
        ])


def generar_ejemplo(num):
    base = {
        1: (15, 5),
        2: (5, 5),
        3: (3, 5)
    }
    a, b = base[num]
    return f""".text
.global _start

_start:
    MOV R0, #{a}
    MOV R1, #{b}

    ADD R2, R0, R1
    SUB R3, R0, R1

    CMP R2, R3
    BGT mayor
    BLT menor
    BEQ iguales

mayor:
    LDR R0, =msg_mayor
    BL print_string
    B fin

menor:
    LDR R0, =msg_menor
    BL print_string
    B fin

iguales:
    LDR R0, =msg_iguales
    BL print_string

fin:
    MOV R7, #1
    MOV R0, #0
    SWI 0

.data
msg_mayor: .asciz "Rama mayor ejecutada\\n"
msg_menor: .asciz "Rama menor ejecutada\\n"
msg_iguales: .asciz "Rama iguales ejecutada\\n"

.text
print_string:
    MOV R7, #4
    MOV R1, R0
    MOV R2, #100
    SWI 0
    BX LR
"""


def main():
    start = time.time()
    source = """
        resultado = a + b
        if a<b (print("a es menor que b"))
        if a>b (print("a es mayor que b"))
        resultado = a * b
        resultado = a - b
    """

    try:
        lexer = LexicalAnalyzer()
        tokens = lexer.tokenize(source)
        parser = SyntacticAnalyzer(tokens)
        stmts = parser.parse()

        gen = AsmGenerator()
        asm_code = gen.generar_codigo(stmts)

        for i in range(1, 4):
            with open(f"sample{i}.s", "w") as f:
                f.write(generar_ejemplo(i))

        with open("ejemplo_generado.s", "w") as f:
            f.write(asm_code)

        print("Código generado con éxito")
        print(asm_code)

    except Exception as e:
        print("Error:", e)

    print(f"Tiempo de ejecución: {(time.time() - start)*1000:.2f} ms")


if __name__ == "__main__":
    main()
