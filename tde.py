from io import TextIOWrapper
from tokens import Token
from palavras_reservadas import palavra_reservada, reservadas
from geradores import gera_temp, gera_label
from lexico import Lexico


class Main:
    def __init__(self):
        with open('arquivo.c') as arq:
            self.lexico = Lexico(arq)
            self.lexico.le_token()
            resultado = ""

            while (self.lexico.token != Token.TK_Fim_Arquivo):
                try:
                    # [com_c, com_p] = self.E()
                    com_p = self.E()
                    resultado += com_p

                except:
                    print(f"[Erro - Main] Algo deu errado.")
                    break
            for part in resultado.split('   '):
                print(part)

    # Parte nova

    # int Lista_Com(char Lista_Com_c[MAX_COD], char lblbreak[])
    def lista_com(self, label_break: str):
        print('Entrei no lista_com')
        print(f'Vou testar Com - token: {self.lexico.token.name}')
        if (self.lexico.token == Token.TK_Fim_Arquivo):
            return None
        if (self.lexico.token not in [Token.TK_id, Token.TK_pv, Token.TK_if, Token.TK_while]):
            return ""

        # if (Com(Com_c, lblbreak)) { ... }
        com_c = self.Com('', label_break)
        if com_c is not None:
            print(f'B - token: {self.lexico.token.name}')
            LL_c = self.lista_com(label_break)
            if LL_c is not None:
                print('Vou retornar no Lista_Com. Token: ',
                      self.lexico.token.name)
                return f"{com_c}{LL_c}"
            else:
                print('Vou retornar None no lista_Com-1. Token: ',
                      self.lexico.token.name)
                return None
        if (self.lexico.token == Token.TK_Fim_Arquivo):
            return ''

        print('Vou retornar None no Lista_Com-2')
        return None

    # Com -> IF ( Rel ) Com ELSE com
    # int Com(char Com_c[MAX_COD], char lblbreak[]) { ... }
    # def Com(self, com_c: str, label_break: str):

    def Com(self, com_c: str, label_break: str):
        print('Entrei no Com')
        Rel_c = ''
        if (self.lexico.token == Token.TK_break):
            self.lexico.le_token()
            if (self.lexico.token == Token.TK_pv):
                self.lexico.le_token()
                return f"{com_c}\tgoto{label_break}"
            else:
                print('[Erro - Com] Faltou o ponto e virgula apos o break')
                return None
        elif (self.lexico.token == Token.TK_if):
            label_else = gera_label()
            label_fim = gera_label()
            self.lexico.le_token()

            # if (Rel(Rel_c)) { ... }
            rel_c = self.Rel()
            if (rel_c is not None):
                if self.lexico.token == Token.TK_Fecha_Par:
                    self.lexico.le_token()
                    com3_c = self.Com('', label_break)
                    if (com3_c is not None):
                        if self.lexico.token == Token.TK_else:
                            self.lexico.le_token()
                            com2_c = self.Com('', label_break)
                            if com2_c is not None:

                                # sprintf(Com_c, "%s\tgofalse %s\n%s\tgoto %s\nrotulo %s\n%srotulo %s\n",
                                #         Rel_c, labelelse, Com3_c, labelfim, labelelse, Com2_c, labelfim);
                                return f"{Rel_c}\tgofalse {label_else}\n{com3_c}\tgoto {label_fim}\nrotulo {label_else}\n{com2_c}rotulo {label_fim}\n"
                            else:
                                print("[Erro: Com if] Erro no comando do Else")
                        else:
                            # sprintf(Com_c, "%s\tgofalse %s\n%srotulo %s\n",
                            #     Rel_c, labelelse, Com3_c, labelelse);
                            return f"{rel_c}\tgofalse {label_else}\n{com3_c}rotulo {label_else}\n"
                    else:
                        print(
                            f"[Erro: Com if] Esperava fecha parênteses. Token: {self.lexico.token.name}")
                else:
                    print("[Erro: Com if] Erro na expressao do if")
            else:
                print(
                    f"[Erro: Com if] Esperava abre parênteses. Token: {self.lexico.token.name}")
            return None
        elif (self.lexico.token == Token.TK_while):
            label_inicio = gera_label()
            label_fim = gera_label()
            self.lexico.le_token()
            if (self.lexico.token == Token.TK_Abre_Par):
                self.lexico.le_token()
                rel_c = self.Rel()
                if (rel_c is not None):
                    if (self.lexico.token == Token.TK_Fecha_Par):
                        self.lexico.le_token()
                        com1_c = self.Com('', label_fim)
                        if (com1_c is not None):
                            # sprintf(Com_c, "rotulo %s\n%s\tgofalse %s\n%s\tgoto %s\nrotulo %s\n",
                            #         labelinicio, Rel_c, labelfim, Com1_c, labelinicio, labelfim);
                            return f"rotulo {label_inicio}\n{rel_c}\tgofalse {label_fim}\n{com1_c}\tgoto {label_inicio}\nrotulo {label_fim}\n"
                        else:
                            print('[Erro - Com while] esperava fecha parênteses')
                    else:
                        print('[Erro - Com while] erro na condicao do while')
                else:
                    print('[Erro - Com while] ?')
            else:
                print(
                    f"[Erro: Com while] Esperava abre parênteses. Token: {self.lexico.token.name}")
            return None
        elif self.lexico.token == Token.TK_id:
            id = self.lexico.lex
            self.lexico.le_token()
            if self.lexico.token == Token.TK_Atrib:
                self.lexico.le_token()
                E_c = self.Rel()
                if E_c is not None:
                    if self.lexico.token == Token.TK_pv:
                        self.lexico.le_token()
                        return f"\tvalor-l {id}\n{E_c}\t:=\n\tpop\n"

                    else:
                        print(
                            '[Erro: Com id] Faltou ponto e virgula apos atribuicao')
                return None

        elif self.lexico.token == Token.TK_Abre_Chaves:
            # todo: abre chaves
            lista_com_c = ""
            self.lexico.le_token()
            print("Consumi o abre chaves")
            lista_com_c = self.lista_com('', label_break)
            if lista_com_c is not None:
                print(f'Voltei do Lista_Com. Token: {self.lexico.token}')
                if (self.lexico.token == Token.TK_Fecha_Chaves):
                    self.lexico.le_token()
                    print('Consumi o fecha chaves')
                    return lista_com_c
                else:
                    print("[Erro: Com abre chave] esperava fecha chave")
                    return None
        elif self.lexico.token == Token.TK_pv:
            print('Vou retornar no Com com ponto e virgula')
            self.lexico.le_token()
            return ''
        else:
            print(f'Vou retornar com vazio. Token: {self.lexico.token.name}')
            return None

    # int Rel(char Rel_c[MAX_COD])
    def Rel(self) -> str or None:
        print('Entrei no Rel')
        E1_c = self.E()
        if (E1_c is not None):
            op = ''
            if (self.lexico.token == Token.TK_Maior):
                op = ">"
            elif (self.lexico.token == Token.TK_Menor):
                op = "<"
            elif (self.lexico.token == Token.TK_Igual):
                op = "="
            elif (self.lexico.token == Token.TK_Diferente):
                op = "<>"
            elif (self.lexico.token == Token.TK_Maior_Igual):
                op = ">="
            elif (self.lexico.token == Token.TK_Menor_Igual):
                op = "<="
            print(f'Voltei do E, token: {self.lexico.token.name} op: {op}')
            if (self.lexico.token in [Token.TK_Maior, Token.TK_Menor, Token.TK_Igual, Token.TK_Diferente, Token.TK_Maior_Igual, Token.TK_Menor_Igual]):
                self.lexico.le_token()
                E2_c = self.E()
                if (E2_c is not None):
                    print(
                        f'Voltei do E2, token: {self.lexico.token.name} op: {op}')
                    return f"{E1_c}{E2_c}\t{op}\n"
                return None
            else:
                return E1_c
        else:
            return None

    # Fim parte nova

    # avalia atribuicao
    def A(self):
        try:
            [E_p, E_c] = self.E()
            if (self.lexico.token != Token.TK_Atrib):
                return [E_p, E_c]
            self.lexico.le_token()
            [A1_p, A1_c] = self.A()
            A_c = f"{A1_c}   {E_p} = {A1_p}"
            A_p = E_p
            return [A_p, A_c]

        except:
            print(f"[Erro - A] token: {self.lexico.token.name}")
            return None

    # avalia expressao
    def E(self):
        try:

            [T_p, T_c] = self.T()
            [R_sp, R_sc] = self.R(T_p, T_c)
            [L_sp, L_sc] = self.L(R_sp, R_sc)
            [Q_sp, Q_sc] = self.Q(L_sp, L_sc)
            return Q_sc
        except:
            print(f"[Erro - E] token: {self.lexico.token.name}")

    # atribuicao, mais igual, menos igual
    def Q(self, R_hp: str, R_hc: str):
        try:
            if (self.lexico.token == Token.TK_Atrib):
                self.lexico.le_token()
                [T_p, T_c] = self.A()
                R1_hp = gera_temp()
                R1_hc = f"{R_hc}{T_c}   {R_hp} = {T_p}"
                return self.R(R1_hp, R1_hc)

            if (self.lexico.token in [Token.TK_Mais_Ig, Token.TK_Menos_Ig]):
                op = '+' if self.lexico.token == Token.TK_Mais_Ig else '-'
                self.lexico.le_token()
                [T_p, T_c] = self.A()
                R1_hp = gera_temp()
                R1_hc = f"{R1_hp} = {R_hc}{R_hp}{T_p}{R1_hp} = {R1_hp} {op} {R_hc}{T_c}"
                return self.R(R1_hp, R1_hc)

        except:
            print("[Erro - Q] token: ", self.lexico.token.name)
            return None

        return [R_hp, R_hc]

    # igual, diferente, maior igual, menor igual
    def L(self, R_hp, R_hc):
        if (self.lexico.token in [Token.TK_Igual, Token.TK_Diferente,
                                  Token.TK_Maior_Igual, Token.TK_Menor_Igual, Token.TK_Maior, Token.TK_Menor]):
            op = ''
            if (self.lexico.token == Token.TK_Igual):
                op = '=='
            elif (self.lexico.token == Token.TK_Diferente):
                op = '!='
            elif (self.lexico.token == Token.TK_Maior_Igual):
                op = '>='
            elif (self.lexico.token == Token.TK_Menor_Igual):
                op = '<='
            elif (self.lexico.token == Token.TK_Maior):
                op = '>'
            elif (self.lexico.token == Token.TK_Menor):
                op = '<'
            self.lexico.le_token()
            try:
                [T_p, T_c] = self.T()
                R1_hp = gera_temp()
                R1_hc = f"{R_hc}{T_c}   {R1_hp} = {R_hp} {op} {T_p}"
                [R_sp, R_sc] = self.R(R1_hp, R1_hc)
                return [R_sc, R_sp] if (self.lexico.flag_igual) else [R_sp, R_sc]
            except:
                print(f"[Erro - L] token: {self.lexico.token.name}")
                return None

        return [R_hp, R_hc]

    # mais, menos
    def R(self, R_hp: str, R_hc: str):
        op = ''
        if (self.lexico.token in [Token.TK_Mais, Token.TK_Menos]):
            op = '+' if self.lexico.token == Token.TK_Mais else '-'
            self.lexico.le_token()
            try:
                [T_p, T_c] = self.T()
                R1_hp = gera_temp()
                R1_hc = f"{R_hc}{T_c}   {R1_hp} = {R_hp} {op} {T_p}"
                return self.R(R1_hp, R1_hc)
            except:
                print(f"[Erro - R] token: {self.lexico.token.name}")

        return [R_hp, R_hc]

    def T(self):
        try:
            [F_p, F_c] = self.F()
            return self.S(F_p, F_c)
        except:
            print(f"[Erro - T] token: {self.lexico.token.name}")
            return None

    # multiplicacao, divisao, resto
    def S(self, S_hp: str, S_hc: str):
        op = ''
        if (self.lexico.token in [Token.TK_Mult, Token.TK_Div, Token.TK_Rest_Div]):
            if (self.lexico.token == Token.TK_Mult):
                op = '*'
            elif (self.lexico.token == Token.TK_Div):
                op = '/'
            elif (self.lexico.token == Token.TK_Rest_Div):
                op = '%'

            self.lexico.le_token()
            try:
                [F_p, F_c] = self.F()
                S1_hp = gera_temp()
                S1_hc = f"{S_hc}{F_c}   {S1_hp} = {S_hp} {op} {F_p}"
                return self.S(S1_hp, S1_hc)

            except:
                print(f"[Erro - S] Erro! token: {self.lexico.token.name}")
                return None

        else:
            return [S_hp, S_hc]

    # cte int, id, parenteses
    def F(self):
        if (self.lexico.token == Token.TK_Const_Int):
            F_p = gera_temp()
            F_c = f"   {F_p} = {self.lexico.lex}"
            self.lexico.le_token()
            return [F_p, F_c]

        if (self.lexico.token in [Token.TK_id, Token.TK_pv, Token.TK_int, Token.TK_float]):
            F_p = self.lexico.lex
            self.lexico.le_token()
            return [F_p, '']

        if (self.lexico.token == Token.TK_Abre_Par):
            self.lexico.le_token()

            try:
                [F_p, F_c] = self.E()

                if (self.lexico.token == Token.TK_Fecha_Par):
                    self.lexico.le_token()
                    return [F_p, F_c]
                else:
                    print("[Erro - F] Esperava fecha parenteses")
            except:
                print(f"[Erro - F] token: {self.lexico.token.name}")

        print(f"[Erro - F] token: {self.lexico.token.name}")
        return None


if __name__ == "__main__":
    Main()
