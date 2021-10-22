from io import TextIOWrapper
from tokens import Token
from palavras_reservadas import reservadas, palavra_reservada


class Lexico:
    def __init__(self, arquivo: TextIOWrapper):
        self.arquivo = arquivo
        self.token = ''
        self.lex = ''
        self.flag_igual = False

        self.estado = 0
        self.c = '\0'

    def le_token(self):
        self.token = self.__le_token()
        return self.token

    def __le_char(self):
        lido = self.arquivo.read(1)
        if (lido != ''):
            return lido
        else:
            return '~'

    def __le_token(self):

        while (True):

            if (self.estado == 0):
                if (self.c == ','):
                    self.c = self.__le_char()
                    return Token.TK_virgula

                if (self.c == '+'):
                    self.c = self.__le_char()
                    if (self.c == '='):
                        self.c = self.__le_char()
                        return Token.TK_Mais_Ig
                    return Token.TK_Mais

                if (self.c == '-'):
                    self.c = self.__le_char()
                    if (self.c == '='):
                        self.c = self.__le_char()
                        return Token.TK_Menos_Ig
                    return Token.TK_Menos

                if (self.c == '/'):
                    self.c = self.__le_char()
                    return Token.TK_Div

                if (self.c == '%'):
                    self.c = self.__le_char()
                    return Token.TK_Rest_Div

                if (self.c == '*'):
                    self.c = self.__le_char()
                    return Token.TK_Mult

                if (self.c == '{'):
                    self.c = self.__le_char()
                    return Token.TK_Abre_Chaves

                if (self.c == '}'):
                    self.c = self.__le_char()
                    return Token.TK_Fecha_Chaves

                if (self.c == ';'):
                    self.c = self.__le_char()
                    self.lex = ';'
                    return Token.TK_pv

                if (self.c == '['):
                    self.c = self.__le_char()
                    return Token.TK_Abre_Colch

                if (self.c == ']'):
                    self.c = self.__le_char()
                    return Token.TK_Fecha_Colch

                if (self.c == '('):
                    self.c = self.__le_char()
                    return Token.TK_Abre_Par

                if (self.c == ')'):
                    self.c = self.__le_char()
                    return Token.TK_Fecha_Par

                if (self.c == '='):
                    self.c = self.__le_char()
                    if (self.c == '='):
                        self.c = self.__le_char()
                        self.flag_igual = True
                        return Token.TK_Igual
                    self.lex = '='
                    return Token.TK_Atrib

                if (self.c == '<'):
                    self.c = self.__le_char()
                    if (self.c == '='):
                        self.c = self.__le_char()
                        return Token.TK_Menor_Igual
                    return Token.TK_Menor

                if (self.c == '>'):
                    self.c = self.__le_char()
                    if (self.c == '='):
                        self.c = self.__le_char()
                        return Token.TK_Maior_Igual
                    return Token.TK_Maior

                if (self.c == '&'):
                    self.c = self.__le_char()
                    if (self.c == '&'):
                        self.c = self.__le_char()
                        return Token.TK_and_logico
                    return Token.TK_and_bitwise

                if (self.c == '!'):
                    self.c = self.__le_char()
                    if (self.c == '='):
                        self.c = self.__le_char()
                        return Token.TK_Diferente

                if (self.c >= 'a' and self.c <= 'z' or self.c >= 'A' and self.c <= 'Z' or self.c == '_'):
                    self.lex = self.c
                    self.c = self.__le_char()
                    self.estado = 1
                    print(self.estado)
                    continue

                if (self.c >= '0' and self.c <= '9'):
                    self.lex = self.c
                    self.c = self.__le_char()
                    self.estado = 2
                    continue

                if (self.c == '~'):
                    return Token.TK_Fim_Arquivo

                if (self.c == '\n' or self.c == '\r' or self.c == '\t' or self.c == '\0' or self.c == ' '):
                    self.c = self.__le_char()
                    continue

            elif (self.estado == 1):
                if (self.c >= 'a' and self.c <= 'z' or self.c >= 'A' and self.c <= 'Z' or self.c == '_' or self.c >= '0' and self.c <= '9'):
                    self.lex += self.c
                    self.c = self.__le_char()
                    continue
                else:
                    self.estado = 0
                    return palavra_reservada(self.lex)

            elif (self.estado == 2):
                if (self.c >= '0' and self.c <= '9'):
                    self.lex += self.c
                    self.c = self.__le_char()
                    continue

                else:
                    self.estado = 0
                    return Token.TK_Const_Int
