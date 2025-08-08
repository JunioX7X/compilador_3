from lexer import TokenType

class SyntacticAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current = tokens[0] if tokens else None

    def _advance(self):
        """Mueve al siguiente token."""
        self.pos += 1
        self.current = self.tokens[self.pos] if self.pos < len(self.tokens) else None
        print(f"[DEBUG] Avanzando a: {self.current}")

    def _match(self, token_type):
        """Consume el token si coincide con el tipo esperado."""
        if self.current and self.current.type == token_type:
            token = self.current
            self._advance()
            return token
        return None

    def parse(self):
        if not self.tokens:
            raise SyntaxError("No hay tokens para analizar")

        statements = []
        while self.current:
            if self.current.type == TokenType.IF:
                statements.append(self._parse_if())
            elif self.current.type == TokenType.PRINT:
                statements.append(self._parse_print())
            elif self.current.type == TokenType.IDENTIFIER:
                statements.append(self._parse_assignment_or_sentence())
            else:
                statements.append(self._parse_sentence())
        return [stmt for stmt in statements if stmt]

    # ---------- Reglas de Gramática ----------
    def _parse_sentence(self):
        noun_phrase = self._parse_noun_phrase()
        if not noun_phrase:
            return None

        verb_phrase = self._parse_verb_phrase()
        if not verb_phrase:
            return None

        if not self._match(TokenType.DOT):
            return None

        return ("sentence", noun_phrase, verb_phrase)

    def _parse_noun_phrase(self):
        article = self._match(TokenType.ARTICLE)
        if not article:
            return None

        adjectives = self._parse_adjective_list()
        noun = self._match(TokenType.NOUN)
        if not noun:
            raise SyntaxError("Se esperaba un sustantivo")

        return ("noun_phrase", article.value, adjectives, noun.value)

    def _parse_adjective_list(self):
        adjectives = []
        while self.current and self.current.type == TokenType.ADJECTIVE:
            adjectives.append(self.current.value)
            self._advance()
        return adjectives

    def _parse_verb_phrase(self):
        verb = self._match(TokenType.VERB)
        if not verb:
            return None
        prep_phrase = self._parse_prep_phrase()
        return ("verb_phrase", verb.value, prep_phrase)

    def _parse_prep_phrase(self):
        if self.current and self.current.type == TokenType.PREPOSITION:
            prep = self.current
            self._advance()
            noun_phrase = self._parse_noun_phrase()
            if not noun_phrase:
                raise SyntaxError("Se esperaba una frase nominal después de la preposición")
            return ("prep_phrase", prep.value, noun_phrase)
        return None

    def _parse_if(self):
        if not self._match(TokenType.IF):
            return None

        left = self._match(TokenType.IDENTIFIER)
        if not left:
            raise SyntaxError("Se esperaba un identificador después de 'if'")

        if self.current and self.current.type in (TokenType.LT, TokenType.GT):
            comp_op = self.current
            self._advance()
        else:
            raise SyntaxError("Se esperaba '<' o '>'")

        right = self._match(TokenType.IDENTIFIER)
        if not right:
            raise SyntaxError("Se esperaba un identificador después del operador de comparación")

        if not self._match(TokenType.LPAREN):
            raise SyntaxError("Se esperaba '('")

        statement = self._parse_print()
        if not statement:
            raise SyntaxError("Se esperaba una sentencia print dentro del if")

        if not self._match(TokenType.RPAREN):
            raise SyntaxError("Se esperaba ')' al final del if")

        return ("if", left.value, comp_op.value, right.value, statement)

    def _parse_print(self):
        if not self._match(TokenType.PRINT):
            return None

        if not self._match(TokenType.LPAREN):
            raise SyntaxError("Se esperaba '(' después de 'print'")

        string = self._match(TokenType.STRING)
        if not string:
            raise SyntaxError("Se esperaba una cadena después de 'print'")

        if not self._match(TokenType.RPAREN):
            raise SyntaxError("Se esperaba ')' después de la cadena")

        return ("print", string.value)

    def _parse_assignment(self):
        target = self._match(TokenType.IDENTIFIER)
        if not target:
            return None

        if not self._match(TokenType.EQ):
            return None

        left = self._match(TokenType.IDENTIFIER)
        if not left:
            raise SyntaxError("Se esperaba un identificador después de '='")

        if self.current and self.current.type in (TokenType.PLUS, TokenType.MINUS, TokenType.MULT):
            op = self.current
            self._advance()
        else:
            raise SyntaxError("Se esperaba un operador (+, -, *)")

        right = self._match(TokenType.IDENTIFIER)
        if not right:
            raise SyntaxError("Se esperaba un identificador después del operador")

        return ("assignment", target.value, left.value, op.value, right.value)

    def _parse_assignment_or_sentence(self):
        if (self.current and
            self.pos + 1 < len(self.tokens) and
            self.tokens[self.pos + 1].type == TokenType.EQ):
            return self._parse_assignment()
        return self._parse_sentence()


def analyze_syntactic(tokens):
    return SyntacticAnalyzer(tokens).parse()
