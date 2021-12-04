from tokens import Token

reservadas = {
    "int": Token.TK_int,
    "float": Token.TK_float,
    "char": Token.TK_char,
    "void": Token.TK_void,
    "struct": Token.TK_struct,
    "if": Token.TK_if,
    "else": Token.TK_else,
    "while": Token.TK_while,
    "for": Token.TK_for,
    "break": Token.TK_break,
    "continue": Token.TK_continue,
    "return": Token.TK_return
}


def palavra_reservada(lex: str):
    if lex in reservadas.keys():
        return reservadas[lex]
    return Token.TK_id
