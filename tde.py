from io import TextIOWrapper
from token import Token


label_num = 0
temp_num = 0
reservadas = {
    "int": Token.TK_int,
    "float": Token.TK_float,
    "char": Token.TK_char,
    "struct": Token.TK_struct,
    "if": Token.TK_if,
    "else": Token.TK_else,
    "while": Token.TK_while
}


def gera_label():
    global label_num
    label_num += 1
    return f"LB00{label_num}"


def gera_temp():
    global temp_num
    temp_num += 1
    return f"LB00{temp_num}"


def le_char(arq: TextIOWrapper):
    c = arq.read(1)
    return c


def pal_res(lex: str):
    if lex in reservadas.keys():
        return reservadas[lex]
    return Token.TK_id


if __name__ == "__main__":
    print('main')

    print(pal_res("int"))
    print(pal_res("float"))
