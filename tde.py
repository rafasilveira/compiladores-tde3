from io import TextIOWrapper
from tokens import Token
from palavras_reservadas import palavra_reservada, reservadas
from geradores import gera_temp, gera_label
from lexico import Lexico


class Main:
    def __init__(self):
        with open('/Users/rafael/ucs/compiladores-tde3/arquivo.c') as arq:
            self.lexico = Lexico(arq)
            self.lexico.le_token()
            try:
                [com_p, com_c] = self.E()
                for part in com_p.split('   '):
                    print(part)
            except:
                print(f"[Erro - Main] Algo deu errado.")
                print(f"token: {self.lexico.token}")

    def A(self):
        try:
            [E_p, E_c] = self.E()
            if (self.lexico.token != Token.TK_Atrib):
                return [E_p, E_c]
            self.lexico.le_token()
            [A1_p, A1_c] = self.A()
            A_c = f"{A1_c}   {E_p} = {A1_p}"
            A_p = E_p

        except:
            print(f"[Erro - A] token: {self.lexico.token}")
            return None

        return [A_p, A_c]

    def E(self):
        try:
            [T_p, T_c] = self.T()
            [R_sc, R_sp] = self.R(T_p, T_c)
            [L_sc, L_sp] = self.L(R_sp, R_sc)
            return self.Q(L_sp, L_sc)
        except:
            print(f"[Erro - Q] token: {self.lexico.token}")

    def Q(self, R_hp: str, R_hc: str):
        try:
            if (self.lexico.token == Token.TK_Atrib):
                self.lexico.le_token()
                [T_p, T_c] = self.A()
                R1_hp = gera_temp()
                R1_hc = f"{R1_hp} = {R_hc}{T_c}   {R1_hp} = {R_hp}{T_p}\n"
                return self.R(R1_hp, R1_hc)
            
            if (self.lexico.token == Token.TK_Mais_Ig):
                self.lexico.le_token()
                [T_p, T_c] = self.A()
                R1_hp = gera_temp()
                R1_hc = f"{R1_hp} = {R_hc}{R_hp}{T_p}{R1_hp} = {R1_hp} + {R_hc}{T_c}\n"
                return self.R(R1_hp, R1_hc)
            
            if (self.lexico.token == Token.TK_Menos_Ig):
                self.lexico.le_token()
                [T_p, T_c] = self.A()
                R1_hp = gera_temp()
                R1_hc = f"{R1_hp} = {R_hc}{R_hp}{T_p}{R1_hp} = {R1_hp} - {R_hc}{T_c}\n"
                return self.R(R1_hp, R1_hc)
        except:
            print("[Erro - Q] Algo deu errado")
            return None
        
        return [R_hp, R_hc]

    def L(self, R_hp, R_hc):
        if (self.lexico.token == Token.TK_Igual):
            self.lexico.le_token()
            try:
                [T_p, T_c] = self.T()
                R1_hp = gera_temp()
                R1_hc = f"{R_hp}{T_c}   {R1_hp} = {R_hc} == {T_p}\n"
                [R_sp, R_sc] = self.R(R1_hp, R1_hc)
                return [R_sc, R_sp] if (self.lexico.flag_igual) else [R_sp, R_sc]
            except:
                print(f"[Erro - L] token: {self.lexico.token}")
                return None

        return [R_hp, R_hc]

    def R(self, R_hp: str, R_hc: str):
        op = ''
        if (self.lexico.token in [Token.TK_Mais, Token.TK_Menos]):
            op = '+' if self.lexico.token == Token.TK_Mais else '-'
            self.lexico.le_token()
            try:
                [T_p, T_c] = self.T()
                R1_hp = gera_temp()
                R1_hc = f"{R_hc}{T_c}   {R1_hp} = {R_hp} {op} {T_p} + \n"
                return self.R(R1_hp, R1_hc)
            except:
                print(f"[Erro - R] token: {self.lexico.token}")

        return [R_hp, R_hc]

    def T(self):
        try:
            [F_p, F_c] = self.F()
            return self.S(F_p, F_c)
        except:
            print(f"[Erro - T] token: {self.lexico.token}")
            return None

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
                print(f"[Erro - S] Erro! token: {self.lexico.token}")
                return None

        else:
            return [S_hp, S_hc]

    def F(self):
        if (self.lexico.token == Token.TK_Const_Int):
            F_p = gera_temp()
            F_c = f"   {F_p} = {self.lexico.lex}"
            self.lexico.le_token()
            return [F_p, F_c]

        if (self.lexico.token == Token.TK_id):
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
                print(f"[Erro - F] token: {self.lexico.token}")

        print(f"[Erro - F] token: {self.lexico.token}")
        return None


if __name__ == "__main__":
    Main()
