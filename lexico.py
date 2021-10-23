from io import TextIOWrapper
from tokens import Token
from palavras_reservadas import palavra_reservada


class Lexico:
    def __init__(self, arquivo: TextIOWrapper):
        self.arquivo = arquivo
        self.token = ''
        self.lex = ''
        self.flag_igual = False
        self.estado = 0
        self.char_lido = '\0'

    def le_token(self):
        self.token = self.__le_token()
        return self.token

    def __le_char(self):
        lido = self.arquivo.read(1)
        if (lido != ''):
            return lido
        else:
            return '~'

    # funcao auxiliar para uso nos operadores + e -
    def __deve_continuar(self):
        if (self.char_lido >= '0' and self.char_lido <= '9'):
            self.lex = self.char_lido
            self.char_lido = self.__le_char()
            self.estado = 2
            return True

        elif (self.char_lido >= 'a' and self.char_lido <= 'z' or self.char_lido > 'A' and self.char_lido <= 'Z' or self.char_lido >= '0' and self.char_lido <= '9' or self.char_lido == '_'):
            self.lex = self.char_lido
            self.char_lido = self.__le_char()
            self.estado = 1
            return True
        
        return False

    def __le_token(self) -> Token:

        while (True):

            if (self.estado == 0):
                if (self.char_lido == ','):
                    self.char_lido = self.__le_char()
                    return Token.TK_virgula

                if (self.char_lido == '+'):
                    self.char_lido = self.__le_char()
                    if (self.char_lido == '='):
                        self.char_lido = self.__le_char()
                        return Token.TK_Mais_Ig
                    elif (self.__deve_continuar()):
                        continue
                    return Token.TK_Mais

                if (self.char_lido == '-'):
                    self.char_lido = self.__le_char()
                    if (self.char_lido == '='):
                        self.char_lido = self.__le_char()
                        return Token.TK_Menos_Ig
                    elif (self.__deve_continuar()):
                        continue
                    return Token.TK_Menos

                if (self.char_lido == '/'):
                    self.char_lido = self.__le_char()
                    return Token.TK_Div

                if (self.char_lido == '%'):
                    self.char_lido = self.__le_char()
                    return Token.TK_Rest_Div

                if (self.char_lido == '*'):
                    self.char_lido = self.__le_char()
                    return Token.TK_Mult

                if (self.char_lido == '{'):
                    self.char_lido = self.__le_char()
                    return Token.TK_Abre_Chaves

                if (self.char_lido == '}'):
                    self.char_lido = self.__le_char()
                    return Token.TK_Fecha_Chaves

                if (self.char_lido == ';'):
                    self.char_lido = self.__le_char()
                    self.lex = ';'
                    return Token.TK_pv

                if (self.char_lido == '['):
                    self.char_lido = self.__le_char()
                    return Token.TK_Abre_Colch

                if (self.char_lido == ']'):
                    self.char_lido = self.__le_char()
                    return Token.TK_Fecha_Colch

                if (self.char_lido == '('):
                    self.char_lido = self.__le_char()
                    return Token.TK_Abre_Par

                if (self.char_lido == ')'):
                    self.char_lido = self.__le_char()
                    return Token.TK_Fecha_Par

                if (self.char_lido == '='):
                    self.char_lido = self.__le_char()
                    if (self.char_lido == '='):
                        self.char_lido = self.__le_char()
                        self.flag_igual = True
                        return Token.TK_Igual
                    self.lex = '='
                    return Token.TK_Atrib

                if (self.char_lido == '<'):
                    self.char_lido = self.__le_char()
                    if (self.char_lido == '='):
                        self.char_lido = self.__le_char()
                        return Token.TK_Menor_Igual
                    return Token.TK_Menor

                if (self.char_lido == '>'):
                    self.char_lido = self.__le_char()
                    if (self.char_lido == '='):
                        self.char_lido = self.__le_char()
                        return Token.TK_Maior_Igual
                    return Token.TK_Maior

                if (self.char_lido == '&'):
                    self.char_lido = self.__le_char()
                    if (self.char_lido == '&'):
                        self.char_lido = self.__le_char()
                        return Token.TK_and_logico
                    return Token.TK_and_bitwise

                if (self.char_lido == '!'):
                    self.char_lido = self.__le_char()
                    if (self.char_lido == '='):
                        self.char_lido = self.__le_char()
                        return Token.TK_Diferente

                if (self.char_lido >= 'a' and self.char_lido <= 'z' or self.char_lido >= 'A' and self.char_lido <= 'Z' or self.char_lido == '_'):
                    self.lex = self.char_lido
                    self.char_lido = self.__le_char()
                    self.estado = 1
                    continue

                if (self.char_lido >= '0' and self.char_lido <= '9'):
                    self.lex = self.char_lido
                    self.char_lido = self.__le_char()
                    self.estado = 2
                    continue

                if (self.char_lido == '~'):
                    return Token.TK_Fim_Arquivo

                if (self.char_lido == '\n' or self.char_lido == '\r' or self.char_lido == '\t' or self.char_lido == '\0' or self.char_lido == ' '):
                    self.char_lido = self.__le_char()
                    continue

            elif (self.estado == 1):
                if (self.char_lido >= 'a' and self.char_lido <= 'z' or self.char_lido >= 'A' and self.char_lido <= 'Z' or self.char_lido == '_' or self.char_lido >= '0' and self.char_lido <= '9'):
                    self.lex += self.char_lido
                    self.char_lido = self.__le_char()
                    continue
                else:
                    self.estado = 0
                    return palavra_reservada(self.lex)

            elif (self.estado == 2):
                if (self.char_lido >= '0' and self.char_lido <= '9'):
                    self.lex += self.char_lido
                    self.char_lido = self.__le_char()
                    continue

                else:
                    self.estado = 0
                    return Token.TK_Const_Int
