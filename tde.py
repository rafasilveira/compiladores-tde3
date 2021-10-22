from io import TextIOWrapper
from tokens import Token
from palavras_reservadas import palavra_reservada, reservadas
from geradores import gera_temp, gera_label
from lexico import Lexico


class Main:

    def __init__(self):
        with open('/Users/rafael/ucs/compiladores-tde3/arquivo.c') as arq:
            self.lexico = Lexico(arq)

            while (self.lexico.token != Token.TK_Fim_Arquivo):
                self.lexico.le_token()

if __name__ == "__main__":
    Main()
