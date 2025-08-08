import re
from enum import Enum


class TokenKind(Enum):
    """Tipos de tokens reconocidos por el analizador léxico."""
    ARTICLE = "ARTICLE"
    ADJECTIVE = "ADJECTIVE"
    NOUN = "NOUN"
    VERB = "VERB"
    PREPOSITION = "PREPOSITION"
    DOT = "DOT"
    UNKNOWN = "UNKNOWN"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULT = "MULT"
    LT = "LT"
    GT = "GT"
    EQ = "EQ"
    IF = "IF"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    PRINT = "PRINT"
    STRING = "STRING"


class Token:
    """Representa un token con su tipo, valor y posición en el texto."""
    def __init__(self, kind, value, position):
        self._kind = kind
        self._value = value
        self._pos = position

    @property
    def type(self):
        return self._kind

    @property
    def value(self):
        return self._value

    @property
    def position(self):
        return self._pos

    def __repr__(self):
        return f"Token({self._kind}, '{self._value}', {self._pos})"


class Lexer:
    """Analizador léxico para convertir texto en una lista de tokens."""
    def __init__(self):
        self._articles = {"the", "a", "an"}
        self._adjectives = {
            "big", "small", "red", "blue", "green", "old", "young",
            "tall", "short", "happy", "sad"
        }
        self._nouns = {
            "cat", "dog", "house", "car", "book", "table", "chair",
            "man", "woman", "child", "tree", "flower"
        }
        self._verbs = {
            "is", "are", "was", "were", "runs", "walks", "sits",
            "stands", "eats", "drinks", "sleeps", "reads"
        }
        self._preps = {"in", "on", "at", "under", "over", "by", "with", "from", "to"}

        # Tokens de un solo carácter
        self._single_char_map = {
            "+": TokenKind.PLUS,
            "-": TokenKind.MINUS,
            "*": TokenKind.MULT,
            "<": TokenKind.LT,
            ">": TokenKind.GT,
            "=": TokenKind.EQ,
            "(": TokenKind.LPAREN,
            ")": TokenKind.RPAREN,
            ".": TokenKind.DOT
        }

    def _add_token(self, tokens, kind, value, pos):
        tokens.append(Token(kind, value, pos))

    def scan(self, text):
        """
        Procesa el texto y devuelve una lista de tokens.
        """
        text = text.strip()
        pos = 0
        tokens = []

        while pos < len(text):
            char = text[pos]

            # Ignorar espacios
            if char.isspace():
                pos += 1
                continue

            # Cadenas entre comillas
            if char == '"':
                closing = text.find('"', pos + 1)
                if closing == -1:
                    raise ValueError(f"String sin cerrar en posición {pos}")
                contenido = text[pos + 1:closing]
                self._add_token(tokens, TokenKind.STRING, contenido, pos)
                pos = closing + 1
                continue

            # Tokens de un solo carácter
            if char in self._single_char_map:
                self._add_token(tokens, self._single_char_map[char], char, pos)
                pos += 1
                continue

            # Palabras (identificadores o reservadas)
            match_word = re.match(r"[a-zA-Z][a-zA-Z0-9]*", text[pos:])
            if match_word:
                palabra = match_word.group(0)
                low = palabra.lower()

                if low == "if":
                    kind = TokenKind.IF
                elif low == "print":
                    kind = TokenKind.PRINT
                elif low in self._adjectives:
                    kind = TokenKind.ADJECTIVE
                elif low in self._nouns:
                    kind = TokenKind.NOUN
                elif low in self._verbs:
                    kind = TokenKind.VERB
                elif low in self._preps:
                    kind = TokenKind.PREPOSITION
                elif low in self._articles:
                    # Verifica si realmente es artículo
                    next_text = text[pos + len(palabra):].lstrip()
                    next_match = re.match(r"[a-zA-Z][a-zA-Z0-9]*", next_text or "")
                    if next_match and next_match.group(0).lower() in (self._adjectives | self._nouns):
                        kind = TokenKind.ARTICLE
                    else:
                        kind = TokenKind.IDENTIFIER
                else:
                    kind = TokenKind.IDENTIFIER

                self._add_token(tokens, kind, low if kind != TokenKind.IDENTIFIER else palabra, pos)
                pos += len(palabra)
                continue

            # Números
            match_num = re.match(r"\d+", text[pos:])
            if match_num:
                num = match_num.group(0)
                self._add_token(tokens, TokenKind.NUMBER, num, pos)
                pos += len(num)
                continue

            # Caracter desconocido
            raise ValueError(f"Carácter no reconocido '{char}' en posición {pos}")

        return tokens


def run_lexer(source):
    """
    Función de entrada para ejecutar el analizador léxico.
    """
    lex = Lexer()
    return lex.scan(source)

TokenType = TokenKind
