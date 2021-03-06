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
            resultado = []

            comandos = self.read_all()
            if comandos is not None:
                with open('saida.kvmp', 'w') as arq_saida:
                    print('\nResultado:\n')
                    for comando in comandos.split('\n'):
                        resultado.append(comando)
                        print(comando)
                        arq_saida.write(f'{comando}\n')

            else:
                print('Programa encerrado com erro.')

    def read_all(self):
        comandos = ""
        while self.lexico.token != Token.TK_Fim_Arquivo:
            resultado = self.read_function()
            if resultado != "":
                comandos += resultado
            else:
                return None

        return comandos

    def read_function(self):
        label_return = gera_label()
        comandos = ""
        print('[function] Entrei no bloco de function')
        if self.lexico.token in [Token.TK_int, Token.TK_float, Token.TK_char, Token.TK_void]:
            print("[function] Encontrei o return_type")
            self.lexico.le_token()
            if self.lexico.token == Token.TK_id:
                print("[function] Encontrei a function_name")
                function_name = self.lexico.lex
                self.lexico.le_token()
                if self.lexico.token == Token.TK_Abre_Par:
                    print("[function] Encontrei abre parenteses")
                    self.lexico.le_token()
                    while self.lexico.token != Token.TK_Fecha_Par:
                        if self.lexico.token in [Token.TK_int, Token.TK_float, Token.TK_char]:
                            self.lexico.le_token()
                            if self.lexico.token == Token.TK_id:
                                self.lexico.le_token()
                                if self.lexico.token == Token.TK_virgula:
                                    self.lexico.le_token()
                                    continue
                                else:
                                    break
                        else:
                            print("[function] tipo de par??metro n??o identificado")
                            print(self.lexico.token)
                            return ""
                    if self.lexico.token == Token.TK_Fecha_Par:
                        print("[function] Encontrei fecha parenteses")
                        self.lexico.le_token()
                        if self.lexico.token == Token.TK_Abre_Chaves:
                            print("[function] Encontrei abre chaves")
                            self.lexico.le_token()
                            comandos += self.lista_com(label_break='',
                                                       label_continue='', label_return=label_return)
                            if self.lexico.token == Token.TK_Fecha_Chaves:
                                print("[function] Encontrei fecha_chaves\n")
                                self.lexico.le_token()
                                list_resultado = '\n'.join([f"    {r}" for r in comandos.split('\n')])
                                inicio_funcao = "\n    push BP\n    BP = SP\n    SP = SP - 16\n"
                                fim_funcao = f"\n\n    rotulo {label_return}\n    leave\n    ret\n\n"
                                return f"{function_name}:{inicio_funcao}{list_resultado}{fim_funcao}"
                else:
                    print("[function] Erro no reconhecimento de abre_parenteses")
                    return ""
            else:
                print("[function] Erro de sintaxe em function_name")
                return ""
        else:
            return ""

    # int Lista_Com(char Lista_Com_c[MAX_COD], char lblbreak[])
    def lista_com(self, label_break: str = '', label_continue: str = '', label_return: str = ''):
        print('Entrei no lista_com')
        print(f'Vou testar Com - token: {self.lexico.token.name}')
        if self.lexico.token == Token.TK_Fim_Arquivo:
            return ''
        if (self.lexico.token not in [Token.TK_id, Token.TK_pv, Token.TK_if, Token.TK_while, Token.TK_break,
                                      Token.TK_continue, Token.TK_for, Token.TK_int, Token.TK_float, Token.TK_char, Token.TK_return]):
            return ""

        # if (Com(Com_c, lblbreak)) { ... }
        com_c = self.Com_break_if_while('', label_break, label_continue, label_return)
        if com_c is not None:
            print(f'B - token: {self.lexico.token.name}')
            LL_c = self.lista_com(label_break, label_continue, label_return)
            if LL_c is not None:
                print('Vou retornar no Lista_Com. Token: ',
                      self.lexico.token.name)
                return f"{com_c}{LL_c}"
            else:
                print('Vou retornar None no lista_Com-1. Token: ',
                      self.lexico.token.name)
                return None
        if self.lexico.token == Token.TK_Fim_Arquivo:
            return ''

        print('Vou retornar None no Lista_Com-2')
        return None

    def com_for_inicializacao(self, anterior: str = ''):
        print(
            f'[For] avaliando inicializacao. token: {self.lexico.token}, resultado: {anterior}')
        if self.lexico.token == Token.TK_pv:
            self.lexico.le_token()
            return anterior
        else:
            if self.lexico.token == Token.TK_id:
                id = self.lexico.lex
                self.lexico.le_token()
                if self.lexico.token == Token.TK_Atrib:
                    self.lexico.le_token()
                    try:
                        [E1_p, E1_c] = self.Rel()
                        resultado = f"{anterior}{E1_c}\n{id} = {E1_p}"
                        if self.lexico.token == Token.TK_virgula:
                            self.lexico.le_token()
                            return self.com_for_inicializacao(resultado)
                        self.lexico.le_token()
                        return resultado
                    except:
                        print("[Erro: com for] unpack rel (inicializacao)")

    def com_for_condicao(self, anterior: str = '', temp_anterior=''):
        print(f'[For] avaliando condicao. token: {self.lexico.token}')
        if self.lexico.token == Token.TK_pv:
            self.lexico.le_token()
            print(f'[for cond] saindo no pv: [None,{anterior}]')
            return [temp_anterior, anterior]
        else:
            try:
                [E2_p, E2_c] = self.Rel()
                resultado = f"{anterior}{E2_c}"
                if self.lexico.token == Token.TK_virgula:
                    self.lexico.le_token()
                    print(f'[for cond] chamada recursiva: {resultado}')
                    return self.com_for_condicao(resultado, E2_p)
                self.lexico.le_token()
                r = [f"{temp_anterior} && {E2_p}" if temp_anterior !=
                     '' else E2_p, resultado]
                print(f'[for cond] saindo no !virgula: {r}')
                return r
            except:
                print("[Erro: com for] unpack rel (condicao)")

    def com_for_incremento(self, anterior: str = ''):
        print(f'[For] avaliando incremento. token: {self.lexico.token}')
        if self.lexico.token == Token.TK_Fecha_Par:
            self.lexico.le_token()
            print(
                f'[com_for_incremento] saindo no fecha par com token: {self.lexico.token}')
            return anterior
        else:
            # self.lexico.le_token()
            if self.lexico.token == Token.TK_pv:
                self.lexico.le_token()
                return self.com_for_incremento(anterior)
            if self.lexico.token == Token.TK_id:
                self.lexico.le_token()
                if self.lexico.token == Token.TK_Atrib:
                    self.lexico.le_token()
                    try:
                        [E3_p, E3_c] = self.Rel()
                        resultado = f"{anterior}{E3_c}"
                        if self.lexico.token == Token.TK_virgula:
                            self.lexico.le_token()
                            print(
                                f'[com_for_incremento] saindo na virgula com token: {self.lexico.token}')
                            return self.com_for_incremento(resultado)
                        self.lexico.le_token()
                        print(
                            f'[com_for_incremento] saindo no else com token: {self.lexico.token}')
                        return resultado
                    except:
                        print("[Erro: com for] unpack rel (incremento)")
            else:
                print(
                    f'[com_for_incremento] saindo no else final com string vazia e token: {self.lexico.token}')
                return ''

    # Com -> IF ( Rel ) Com ELSE com
    # int Com(char Com_c[MAX_COD], char lblbreak[]) { ... }

    def Com_break_if_while(self, com_c: str, label_break: str = '', label_continue: str = '', label_return: str = ''):
        print('Entrei no Com')
        if self.lexico.token in [Token.TK_break, Token.TK_continue]:
            label = label_break if self.lexico.token is Token.TK_break else label_continue
            op = 'break' if self.lexico.token is Token.TK_break else 'continue'
            self.lexico.le_token()
            if self.lexico.token == Token.TK_pv:
                self.lexico.le_token()
                return f"{com_c}\tgoto {label}\n"
            else:
                print(f'[Erro - Com] Faltou o ponto e virgula apos o {op}')
                return None
        elif self.lexico.token == Token.TK_return:
            print("Encontrou um return")
            self.lexico.le_token()
            resultado_rel = self.Rel()
            if resultado_rel is not None:
                [rel_p, rel_c] = resultado_rel
                if self.lexico.token == Token.TK_pv:
                    self.lexico.le_token()
                    return "\ngoto " + label_return
        elif self.lexico.token == Token.TK_if:
            label_fim = gera_label()
            self.lexico.le_token()

            if self.lexico.token is Token.TK_Abre_Par:
                self.lexico.le_token()
                # if (Rel(Rel_c)) { ... }
                resultado_rel = self.Rel()
                if resultado_rel is not None:
                    [rel_p, rel_c] = resultado_rel
                    if self.lexico.token == Token.TK_Fecha_Par:
                        self.lexico.le_token()
                        com3_c = self.Com_break_if_while(
                            '', label_break, label_continue)
                        print("eu to aqui")
                        if com3_c is not None:
                            com3_c = '\n  '.join(com3_c.split('\n'))
                            if self.lexico.token == Token.TK_else:
                                label_else = gera_label()
                                self.lexico.le_token()
                                com2_c = self.Com_break_if_while(
                                    '', label_break, label_continue)
                                if com2_c is not None:
                                    # com2_c = '\n  '.join(com2_c.split('\n'))
                                    return f"{rel_c}\nif !({rel_p}) goto {label_else}{com3_c}\n\nrotulo {label_else} (else){com2_c}\n\nrotulo {label_fim} (fim if)\n"
                                else:
                                    print(
                                        "[Erro: Com if] Erro no comando do Else")
                            else:
                                return f"\n{rel_c}\nif !({rel_p}) goto {label_fim}\n{com3_c}\nrotulo {label_fim} (fim if)"
                    else:
                        print(
                            f"[Erro: Com if] Esperava fecha par??nteses. Token: {self.lexico.token.name}")
                else:
                    print("[Erro: Com if] Erro na expressao do if")
            else:
                print(
                    f"[Erro: Com if] Esperava abre par??nteses. Token: {self.lexico.token.name}")
            return None
        elif self.lexico.token == Token.TK_while:
            label_inicio = gera_label()
            label_fim = gera_label()
            label_cont = gera_label()
            self.lexico.le_token()
            if self.lexico.token == Token.TK_Abre_Par:
                self.lexico.le_token()
                resultado_rel = self.Rel()
                if resultado_rel is not None:
                    [rel_p, rel_c] = resultado_rel
                    if self.lexico.token == Token.TK_Fecha_Par:
                        self.lexico.le_token()
                        bloco_comandos = self.Com_break_if_while(
                            '', label_break=label_fim, label_continue=label_cont)
                        bloco_comandos = '\n  '.join(
                            bloco_comandos.split('\n'))
                        if bloco_comandos is not None:
                            return f"{rel_c}\nrotulo {label_inicio} (inicio if)\nif !({rel_p}) goto {label_fim}{bloco_comandos}\n\tgoto {label_inicio}\nrotulo {label_fim} (fim if)"

                        else:
                            print('[Erro - Com while] esperava fecha par??nteses')
                    else:
                        print('[Erro - Com while] erro na condicao do while')
                else:
                    print('[Erro - Com while] ?')
            else:
                print(
                    f"[Erro: Com while] Esperava abre par??nteses. Token: {self.lexico.token.name}")
            return None

        elif self.lexico.token == Token.TK_for:
            label_inicio = gera_label()
            label_fim = gera_label()
            label_cont = gera_label()
            self.lexico.le_token()

            if self.lexico.token == Token.TK_Abre_Par:
                self.lexico.le_token()
                com_inicializacao = self.com_for_inicializacao()
                resultado_com_condicao = self.com_for_condicao()
                com_incremento = self.com_for_incremento()

                try:
                    [temp_condicao, com_condicao] = resultado_com_condicao
                    if com_condicao == '':
                        condicao_ou_branco = ''
                    else:
                        condicao_ou_branco = f"{com_condicao}\nif !({temp_condicao}) goto {label_fim}"
                except:
                    condicao_ou_branco = ''

                if self.lexico.token == Token.TK_Fecha_Par:
                    self.lexico.le_token()
                bloco_comandos = self.Com_break_if_while('',
                                                         label_break=label_fim, label_continue=label_cont)
                bloco_comandos = '\n  '.join(bloco_comandos.split('\n'))
                return f"{com_inicializacao}\n\nrotulo {label_inicio}{condicao_ou_branco}\n{bloco_comandos}\n\nrotulo {label_cont}{com_incremento}\n\tgoto {label_inicio}\n\nrotulo {label_fim}"
        elif self.lexico.token in [Token.TK_int, Token.TK_float, Token.TK_char]:
            self.lexico.le_token()
            if self.lexico.token == Token.TK_id:
                id = self.lexico.lex
                self.lexico.le_token()
                if self.lexico.token == Token.TK_Atrib:
                    self.lexico.le_token()
                    resultado_rel = self.Rel()
                    if resultado_rel is not None:
                        [rel_p, rel_c] = resultado_rel
                        if self.lexico.token == Token.TK_pv:
                            self.lexico.le_token()
                            return f"{rel_c}\n{id} = {rel_p}"

                        else:
                            print(
                                '[Erro: Com id] Faltou ponto e virgula apos atribuicao')
                    return None

                if self.lexico.token == Token.TK_pv:
                    self.lexico.le_token()
                    return ""
        elif self.lexico.token == Token.TK_id:
            id = self.lexico.lex
            self.lexico.le_token()

            if self.lexico.token == Token.TK_Abre_Par:
                print("fun????o void")
                self.ler_parametros_funcao()

                if self.lexico.token == Token.TK_pv:
                    self.lexico.le_token()
                    return ""

            if self.lexico.token == Token.TK_Atrib:
                self.lexico.le_token()
                resultado_rel = self.Rel()
                if resultado_rel is not None:
                    [rel_p, rel_c] = resultado_rel
                    if self.lexico.token == Token.TK_pv:
                        self.lexico.le_token()
                        return f"{rel_c}\n{id} = {rel_p}"

                    else:
                        print(
                            '[Erro: Com id] Faltou ponto e virgula apos atribuicao')
                return None
        elif self.lexico.token == Token.TK_Abre_Chaves:
            lista_com_c = ""
            self.lexico.le_token()
            print("Consumi o abre chaves")
            lista_com_c = self.lista_com(label_break, label_continue, label_return)
            if lista_com_c is not None:
                print(f'Voltei do Lista_Com. Token: {self.lexico.token}')
                if self.lexico.token == Token.TK_Fecha_Chaves:
                    self.lexico.le_token()
                    print('Consumi o fecha chaves')
                    return lista_com_c
                else:
                    print(
                        f"[Erro: Com abre chave] esperava fecha chave. Token: {self.lexico.token.name}")
                    return None
            else:
                print('[Erro: Com abre chave] erro no comando')
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
        try:
            [E1_p, E1_c] = self.E_expressao()
            op = ''
            if self.lexico.token == Token.TK_Maior:
                op = ">"
            elif self.lexico.token == Token.TK_Menor:
                op = "<"
            elif self.lexico.token == Token.TK_Igual:
                op = "="
            elif self.lexico.token == Token.TK_Diferente:
                op = "<>"
            elif self.lexico.token == Token.TK_Maior_Igual:
                op = ">="
            elif self.lexico.token == Token.TK_Menor_Igual:
                op = "<="
            print(f'Voltei do E, token: {self.lexico.token.name} op: {op}')
            if (self.lexico.token in [Token.TK_Maior, Token.TK_Menor, Token.TK_Igual, Token.TK_Diferente,
                                      Token.TK_Maior_Igual, Token.TK_Menor_Igual]):
                self.lexico.le_token()
                resultado_E2 = self.E_expressao()
                if resultado_E2 is not None:
                    [E2_p, E2_c] = resultado_E2
                    print(
                        f'Voltei do E2, token: {self.lexico.token.name} op: {op}')
                    return [E2_p, f"{E1_c}{E2_c}\t{op}\n"]
                return None
            else:
                return [E1_p, E1_c]
        except:
            return None

    # avalia atribuicao

    def A(self):
        try:
            [E_p, E_c] = self.E_expressao()
            if self.lexico.token != Token.TK_Atrib:
                return [E_p, E_c]
            self.lexico.le_token()
            [A1_p, A1_c] = self.A()
            A_c = f"{A1_c}\n{E_p} = {A1_p}"
            A_p = E_p
            return [A_p, A_c]

        except:
            print(f"[Erro - A] token: {self.lexico.token.name}")
            return None

    # avalia expressao
    def E_expressao(self):
        try:
            [T_p, T_c] = self.T()
            [R_sp, R_sc] = self.R_mais_menos(T_p, T_c)
            [L_sp, L_sc] = self.L_relacionais(R_sp, R_sc)
            [Q_sp, Q_sc] = self.Q_atr_maisig_menosig(L_sp, L_sc)
            return [Q_sp, Q_sc]
        except:
            print(f"[Erro - E] token: {self.lexico.token.name}")

    # atribuicao, mais igual, menos igual
    def Q_atr_maisig_menosig(self, R_hp: str, R_hc: str):
        try:
            if self.lexico.token == Token.TK_Atrib:
                self.lexico.le_token()
                [T_p, T_c] = self.A()
                R1_hp = gera_temp()
                R1_hc = f"{R_hc}{T_c}\n{R_hp} = {T_p}"
                return self.R_mais_menos(R1_hp, R1_hc)

            if self.lexico.token in [Token.TK_Mais_Ig, Token.TK_Menos_Ig]:
                op = '+' if self.lexico.token == Token.TK_Mais_Ig else '-'
                self.lexico.le_token()
                [T_p, T_c] = self.A()
                R1_hp = gera_temp()
                R1_hc = f"{R1_hp} = {R_hc}{R_hp}{T_p}{R1_hp} = {R1_hp} {op} {R_hc}{T_c}"
                return self.R_mais_menos(R1_hp, R1_hc)

        except:
            print("[Erro - Q] token: ", self.lexico.token.name)
            return None

        return [R_hp, R_hc]

    # igual, diferente, maior igual, menor igual
    def L_relacionais(self, R_hp, R_hc):
        if (self.lexico.token in [Token.TK_Igual, Token.TK_Diferente,
                                  Token.TK_Maior_Igual, Token.TK_Menor_Igual, Token.TK_Maior, Token.TK_Menor]):
            op = ''
            if self.lexico.token == Token.TK_Igual:
                op = '=='
            elif self.lexico.token == Token.TK_Diferente:
                op = '!='
            elif self.lexico.token == Token.TK_Maior_Igual:
                op = '>='
            elif self.lexico.token == Token.TK_Menor_Igual:
                op = '<='
            elif self.lexico.token == Token.TK_Maior:
                op = '>'
            elif self.lexico.token == Token.TK_Menor:
                op = '<'
            self.lexico.le_token()
            try:
                [T_p, T_c] = self.T()
                R1_hp = gera_temp()
                R1_hc = f"{R_hc}{T_c}\n{R1_hp} = {R_hp} {op} {T_p}"
                [R_sp, R_sc] = self.R_mais_menos(R1_hp, R1_hc)
                return [R_sc, R_sp] if self.lexico.flag_igual else [R_sp, R_sc]
            except:
                print(f"[Erro - L] token: {self.lexico.token.name}")
                return None

        return [R_hp, R_hc]

    # mais, menos
    def R_mais_menos(self, R_hp: str, R_hc: str):
        op = ''
        if self.lexico.token in [Token.TK_Mais, Token.TK_Menos]:
            op = '+' if self.lexico.token == Token.TK_Mais else '-'
            self.lexico.le_token()
            try:
                [T_p, T_c] = self.T()
                R1_hp = gera_temp()
                R1_hc = f"{R_hc}{T_c}\n{R1_hp} = {R_hp} {op} {T_p}"
                return self.R_mais_menos(R1_hp, R1_hc)
            except:
                print(f"[Erro - R] unpack T. token: {self.lexico.token.name}")

        return [R_hp, R_hc]

    def T(self):
        try:
            [F_p, F_c] = self.F_cte_id_parenteses()
            return self.S_mult_div_resto(F_p, F_c)
        except:
            print(f"[Erro - T] unpack F. token: {self.lexico.token.name}")
            return None

    # multiplicacao, divisao, resto
    def S_mult_div_resto(self, S_hp: str, S_hc: str):
        op = ''
        if self.lexico.token in [Token.TK_Mult, Token.TK_Div, Token.TK_Rest_Div]:
            if self.lexico.token == Token.TK_Mult:
                op = '*'
            elif self.lexico.token == Token.TK_Div:
                op = '/'
            elif self.lexico.token == Token.TK_Rest_Div:
                op = '%'

            self.lexico.le_token()
            try:
                [F_p, F_c] = self.F_cte_id_parenteses()
                S1_hp = gera_temp()
                S1_hc = f"{S_hc}{F_c}\n{S1_hp} = {S_hp} {op} {F_p}"
                return self.S_mult_div_resto(S1_hp, S1_hc)

            except:
                print(
                    f"[Erro - S] Erro unpack F. token: {self.lexico.token.name}")
                return None

        else:
            return [S_hp, S_hc]

    def ler_parametros_funcao(self):
        print("chamada de fun????o")
        self.lexico.le_token()
        while self.lexico.token != Token.TK_Fecha_Par:
            try:
                self.lexico.le_token()
                prt = self.Rel()
                if prt is not None:
                    if self.lexico.token == Token.TK_virgula:
                        print("Pula para o pr??ximo par??metro")
                        self.lexico.le_token()
                        continue
                    else:
                        break
            except:
                print("Problema na leitura de par??metros da fun????o")
                return None

        self.lexico.le_token()
        print("Leitura de par??metros finalizada", "<-----------------------------------")

    # cte int, id, parenteses
    def F_cte_id_parenteses(self):
        if self.lexico.token == Token.TK_Const_Int:
            F_p = gera_temp()
            F_c = f"\n{F_p} = {self.lexico.lex}"
            self.lexico.le_token()
            return [F_p, F_c]

        if self.lexico.token in [Token.TK_id]:
            print("vari??vel")
            F_p = self.lexico.lex
            self.lexico.le_token()
            if self.lexico.token == Token.TK_Abre_Par:
                print("fun????o")
                self.ler_parametros_funcao()

            return [F_p, '']

        if self.lexico.token in [Token.TK_pv, Token.TK_int, Token.TK_float]:
            F_p = self.lexico.lex
            self.lexico.le_token()
            return [F_p, '']

        if self.lexico.token == Token.TK_Abre_Par:
            self.lexico.le_token()

            try:
                [F_p, F_c] = self.E_expressao()

                if self.lexico.token == Token.TK_Fecha_Par:
                    self.lexico.le_token()
                    return [F_p, F_c]
                else:
                    print("[Erro - F] Esperava fecha parenteses")
            except:
                print(f"[Erro - F] unpack E - token: {self.lexico.token.name}")

        print(f"[Erro - F] token desconhecido: {self.lexico.token.name}")
        return None


if __name__ == "__main__":
    Main()

