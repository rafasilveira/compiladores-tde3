#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TK_int 1
#define TK_float 2
#define TK_char 3
#define TK_struct 4
#define TK_if 5
#define TK_else 6
#define TK_id 7
#define TK_Abre_Colch 8
#define TK_Fecha_Colch 9
#define TK_Abre_Chaves 10
#define TK_Fecha_Chaves 11
#define TK_Fim_Arquivo 12
#define TK_Atrib 13
#define TK_Const_Int 14
#define TK_Mais 15
#define TK_Menos 16
#define TK_Mult 17
#define TK_Divisao 18
#define TK_Resto 19
#define TK_Abre_Par 20
#define TK_Fecha_Par 21
#define TK_virgula 22
#define TK_pv 23
#define TK_Maior 24
#define TK_Menor 25
#define TK_Menor_Igual 26
#define TK_Maior_Igual 27
#define TK_Igual 28
#define TK_Diferente 29
#define TK_while 30
#define TK_and_bitwise 31
#define TK_and_logico 32
#define TK_Mais_Igual 33
#define TK_Menos_Igual 34

/***********************************************************************************/
/*                                                                                 */
/*  IN�CIO DO L�XICO - N�o entre a n�o ser que tenha interesse pessoal em l�xicos  */
/*                                                                                 */
/***********************************************************************************/

int linlex = 0, collex = 1;

char tokens[][30] = {
    "",
    "TK_int",
    "TK_float",
    "TK_char",
    "TK_struct",
    "TK_if",
    "TK_else",
    "TK_id",
    "TK_Abre_Colch",
    "TK_Fecha_Colch",
    "TK_Abre_Chaves",
    "TK_Fecha_Chaves",
    "TK_Fim_Arquivo",
    "TK_Atrib",
    "TK_Const_Int",
    "TK_Mais",
    "TK_Menos",
    "TK_Mult",
    "TK_Divisao",
    "TK_Resto",
    "TK_Abre_Par",
    "TK_Fecha_Par",
    "TK_virgula",
    "TK_pv",
    "TK_Maior",
    "TK_Menor",
    "TK_Menor_Igual",
    "TK_Maior_Igual",
    "TK_Igual",
    "TK_Diferente",
    "TK_while",
    "TK_and_bitwise",
    "TK_and_logico",
    "TK_Mais_Igual",
    "TK_Menos_Igual",
};

typedef struct pal {
  char palavra[20];
  int token;
} tpal;
tpal reservadas[] = {
    {"", 0},
    {"int", TK_int},
    {"float", TK_float},
    {"char", TK_char},
    {"struct", TK_struct},
    {"if", TK_if},
    {"else", TK_else},
    {"while", TK_while},
    {"fim", -1}};

FILE *arqin;
int token;
char lex[20];

// vari�veis do marca - restaura

int tokenant;
long posarq;
char lexant[100];
char cant;
int marcou = 0;

void marca_pos() {
  marcou = 1;
  tokenant = token;
  posarq = ftell(arqin);
  strcpy(lexant, lex);
}

void restaura() {
  fseek(arqin, posarq, SEEK_SET);
  token = tokenant;
  strcpy(lex, lexant);
}

char le_char() {
  char c;

  if (fread(&c, 1, 1, arqin) == 0)
    return -1;
  if (c == '\n') {
    linlex++;
    collex = 1;
  } else
    collex++;
  return c;
};

int pal_res(char lex[]) {
  int tk = 0;
  while (strcmp(reservadas[tk].palavra, "fim") != 0) {
    if (strcmp(lex, reservadas[tk].palavra) == 0)
      return reservadas[tk].token;
    tk++;
  }
  return TK_id;
}

int le_token() {
  static int pos = 0;
  static int estado = 0;
  static char c = '\0';
  while (1) {
    switch (estado) {
      case 0:
        if (c == ',') {
          c = le_char();
          return TK_virgula;
        }
        if (c == '+') {
          c = le_char();
          if (c == '=') {
            c = le_char();
            return TK_Mais_Igual;
          }
          return TK_Mais;
        }
        if (c == '-') {
          c = le_char();
          if (c == '=') {
            c = le_char();
            return TK_Menos_Igual;
          } else
          if (c >= '0' && c <= '9') {
            lex[0] = c;
            c = le_char();
            pos = 1;
            estado = 2;
            break;
          }
          if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9') ||c == '_') {
            lex[0] = c;
            c = le_char();
            pos = 1;
            estado = 1;
            break;
          }
          return TK_Menos;
        }
        if (c == '*') {
          c = le_char();
          return TK_Mult;
        }
        if (c == '/') {
          c = le_char();
          return TK_Divisao;
        }
        if (c == '%') {
          c = le_char();
          return TK_Resto;
        }
        if (c == '{') {
          c = le_char();
          return TK_Abre_Chaves;
        }
        if (c == '}') {
          c = le_char();
          return TK_Fecha_Chaves;
        }
        if (c == ';') {
          c = le_char();
          strcpy(lex, ";");
          return TK_pv;
        }
        if (c == '[') {
          c = le_char();
          return TK_Abre_Colch;
        }
        if (c == ']') {
          c = le_char();
          return TK_Fecha_Colch;
        }
        if (c == '(') {
          c = le_char();
          return TK_Abre_Par;
        }
        if (c == ')') {
          c = le_char();
          return TK_Fecha_Par;
        }
        if (c == '=') {
          c = le_char();
          if (c == '=') {
            c = le_char();
            return TK_Igual;
          }
          strcpy(lex, "=");
          return TK_Atrib;
        }
        if (c == '<') {
          c = le_char();
          if (c == '=') {
            c = le_char();
            return TK_Menor_Igual;
          }
          return TK_Menor;
        }
        if (c == '&&') {
          c = le_char();
          if (c == '&') {
            c = le_char();
            return TK_and_logico;
          }
          return TK_and_bitwise;
        }
        if (c == '>') {
          c = le_char();
          if (c == '=') {
            c = le_char();
            return TK_Maior_Igual;
          }
          return TK_Maior;
        }
        if (c == '!') {
          c = le_char();
          if (c == '=') {
            c = le_char();
            return TK_Diferente;
          }
        }
        if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '_') {
          lex[0] = c;
          c = le_char();
          pos = 1;
          estado = 1;
          break;
        }
        if (c >= '0' && c <= '9') {
          lex[0] = c;
          c = le_char();
          pos = 1;
          estado = 2;
          break;
        }
        if (c == -1)
          return TK_Fim_Arquivo;
        if (c == '\n' || c == '\r' || c == '\t' || c == '\0' || c == ' ') {
          c = le_char();
          break;
        }
      case 1:
        if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '_' || (c >= '0' && c <= '9')) {
          lex[pos++] = c;
          c = le_char();
          break;
        } else {
          estado = 0;
          lex[pos] = '\0';
          return pal_res(lex);
        }
      case 2:
        if (c >= '0' && c <= '9') {
          lex[pos++] = c;
          c = le_char();
          break;
        } else {
          estado = 0;
          lex[pos] = '\0';
          return TK_Const_Int;
        }
    }
  }
}

/********************/
/*                  */
/*  FIM DO L�XICO   */
/*                  */
/********************/

#define MAX_COD 1000

void mostra_t() {
  printf("%s lex = %s na lin %d, col %d\n", tokens[token], lex, linlex, collex);
}

void geralabel(char label[]) {
  static int numlabel = 0;
  sprintf(label, "LB%03d", numlabel++);
}

void geratemp(char temp[]) {
  static int numtemp = 0;
  sprintf(temp, "T%03d", numtemp++);
}

/****************/
/*              */
/*  EXPRESS�ES  */
/*              */
/****************/

int T(char T_p[MAX_COD], char T_c[MAX_COD]);
int E(char E_p[MAX_COD], char E_c[MAX_COD]);
int R(char R_hp[MAX_COD], char R_sp[MAX_COD], char R_hc[MAX_COD], char R_sc[MAX_COD]);
int F(char F_p[MAX_COD], char F_c[MAX_COD]);
int S(char S_hp[MAX_COD], char S_sp[MAX_COD], char S_hc[MAX_COD], char S_sc[MAX_COD]);
int Rel(char Rel_c[MAX_COD], char Rel_true[MAX_COD], char Rel_false[MAX_COD]);

int A(char A_p[MAX_COD], char A_c[MAX_COD]) {
  char A1_p[MAX_COD], A1_c[MAX_COD], E_p[MAX_COD], E_c[MAX_COD];
  char id[100];
  if (!E(E_p, E_c))
    printf("DEBUG: Retornando 0 no A se !E (token: %s)\n", tokens[token]);
  return 0;
  if (token != TK_Atrib) {
    strcpy(A_p, E_p);
    strcpy(A_c, E_c);
    return 1;
  }
  token = le_token();  // consome o sinal de atribui��o
  if (!A(A1_p, A1_c)) {
    printf("DEBUG: Retornando 0 no A se !A (token: %s)\n", tokens[token]);
    return 0;
  }
  sprintf(A_c, "%s\t%s = %s\n", A1_c, E_p, A1_p);
  strcpy(A_p, E_p);
  return 1;
}

int Rel(char Rel_c[MAX_COD], char Rel_true[MAX_COD], char Rel_false[MAX_COD]) {
  char E1_c[MAX_COD], E2_c[MAX_COD], R_sc[MAX_COD], E1_p[MAX_COD], E2_p[MAX_COD], R_sp[MAX_COD];
  if (E(E1_p, E1_c)) {
    char op[10];
    if (token == TK_Maior)
      strcpy(op, ">");
    else if (token == TK_Menor)
      strcpy(op, "<");
    else if (token == TK_Igual)
      strcpy(op, "=");
    else if (token == TK_Diferente)
      strcpy(op, "<>");
    else if (token == TK_Maior_Igual)
      strcpy(op, ">=");
    else if (token == TK_Menor_Igual)
      strcpy(op, "<=");
    else if (token == TK_Mais_Igual)
      strcpy(op, "+=");
    else if (token == TK_Menos_Igual)
      strcpy(op, "-=");
    if (token == TK_Maior || token == TK_Menor || token == TK_Igual || token == TK_Diferente || token == TK_Maior_Igual || token == TK_Menor_Igual) {
      token = le_token();
      if (E(E2_p, E2_c)) {
        sprintf(Rel_c, "%s%s\tif %s %s %s goto %s\n\tgoto %s\n", E1_c, E2_c, E1_p, op, E2_p, Rel_true, Rel_false);
        return 1;
      }
      return 0;
    } else
      return 0;
  }
  return 0;
}

// E -> T { Rhp=Tp   Rhc=Tc}  R   {E.p=RSp   E.c=Rsc}
/* E -> E +T | E - T | T */
int E(char E_p[MAX_COD], char E_c[MAX_COD]) {
  char T_p[MAX_COD], T_c[MAX_COD], R_hp[MAX_COD], R_sp[MAX_COD], R_hc[MAX_COD], R_sc[MAX_COD];
  if (T(T_p, T_c)) {
    strcpy(R_hc, T_c);
    strcpy(R_hp, T_p);
    if (R(R_hp, R_sp, R_hc, R_sc)) {
      strcpy(E_c, R_sc);
      strcpy(E_p, R_sp);
      return 1;
    } else {
      printf("DEBUG: Retornando 0 no E se T e !R\n");
    }
  } else {
    printf("DEBUG: Retornando 0 no E se !T\n");
  }
  return 0;
}

int R(char R_hp[MAX_COD], char R_sp[MAX_COD], char R_hc[MAX_COD], char R_sc[MAX_COD]) {
  char T_c[MAX_COD], R1_hc[MAX_COD], R1_sc[MAX_COD], T_p[MAX_COD], R1_hp[MAX_COD], R1_sp[MAX_COD];
  if (token == TK_Mais) {
    token = le_token();
    if (T(T_p, T_c)) {
      geratemp(R1_hp);
      sprintf(R1_hc, "%s%s\t%s = %s + %s\n", R_hc, T_c, R1_hp, R_hp, T_p);
      if (R(R1_hp, R1_sp, R1_hc, R1_sc)) {
        strcpy(R_sp, R1_sp);
        strcpy(R_sc, R1_sc);
        return 1;
      } else {
        printf("DEBUG: Retornando zero no R se !R (token: %s)\n", tokens[token]);
      }
    } else {
      printf("DEBUG: Retornando zero no R se !T (token: %s)\n", tokens[token]);
    }
    return 0;
  }
  if (token == TK_Menos) {
    token = le_token();
    if (T(T_p, T_c)) {
      geratemp(R1_hp);
      sprintf(R1_hc, "%s%s\t%s = %s - %s\n", R_hc, T_c, R1_hp, R_hp, T_p);
      if (R(R1_hp, R1_sp, R1_hc, R1_sc)) {
        strcpy(R_sp, R1_sp);
        strcpy(R_sc, R1_sc);
        return 1;
      }
    }
    printf("DEBUG: Retornando zero no R se token == tkmenos\n");
    return 0;
  }
  strcpy(R_sp, R_hp);
  strcpy(R_sc, R_hc);
  return 1;
}

/* T -> T * F | F */
int T(char T_p[MAX_COD], char T_c[MAX_COD]) {
  char F_c[MAX_COD], F_p[MAX_COD], S_hp[MAX_COD], S_sp[MAX_COD], S_hc[MAX_COD], S_sc[MAX_COD];
  if (F(F_p, F_c)) {
    strcpy(S_hc, F_c);
    strcpy(S_hp, F_p);
    if (S(S_hp, S_sp, S_hc, S_sc)) {
      strcpy(T_c, S_sc);
      strcpy(T_p, S_sp);
      return 1;
    } else {
      printf("DEBUG: Retornando 0 no T se !S\n");
    }
  } else {
    printf("DEBUG: Retornando 0 no T se !F\n");
  }
  return 0;
}

int S(char S_hp[MAX_COD], char S_sp[MAX_COD], char S_hc[MAX_COD], char S_sc[MAX_COD]) {
  char F_c[MAX_COD], S1_hc[MAX_COD], S1_sc[MAX_COD], F_p[MAX_COD], S1_hp[MAX_COD], S1_sp[MAX_COD];
  switch (token) {
    // atribuicao
    case TK_Atrib: {
      token = le_token();
      if (F(F_p, F_c)) {
        sprintf(S1_hc, "%s%s\t%s = %s\n", S_hc, F_c, S_hp, F_p);
        if (S(S1_hp, S1_sp, S1_hc, S1_sc)) {          
          strcpy(S_sp, S1_sp);
          strcpy(S_sc, S1_sc);
          return 1;
        }
      }
      return 0;
    }

    /************************************/
    /** aritmeticos */
    case TK_Mais_Igual: {
      token = le_token();
      if (F(F_p, F_c)) {
        sprintf(S1_hc, "%s%s\t%s = %s + %s\n", S_hc, F_c, S_hp, S_hp, F_p);
        if (S(S1_hp, S1_sp, S1_hc, S1_sc)) {
          strcpy(S_sp, S1_sp);
          strcpy(S_sc, S1_sc);
          return 1;
        }
      }
      return 0;
    }

    case TK_Menos_Igual: {
      token = le_token();
      if (F(F_p, F_c)) {
        sprintf(S1_hc, "%s%s\t%s = %s - %s\n", S_hc, F_c, S_hp, S_hp, F_p);
        if (S(S1_hp, S1_sp, S1_hc, S1_sc)) {
          strcpy(S_sp, S1_sp);
          strcpy(S_sc, S1_sc);
          return 1;
        }
      }
      return 0;
    }

    // multiplicacao
    case TK_Mult: {
      token = le_token();
      if (F(F_p, F_c)) {
        geratemp(S1_hp);
        sprintf(S1_hc, "%s%s\t%s = %s * %s\n", S_hc, F_c, S1_hp, S_hp, F_p);
        if (S(S1_hp, S1_sp, S1_hc, S1_sc)) {
          strcpy(S_sp, S1_sp);
          strcpy(S_sc, S1_sc);
          return 1;
        } else {
          printf("DEBUG: Retornando 0 no S se F e !S\n");
        }
      } else {
        printf("DEBUG: Retornando 0 no S se !F\n");
      }
      return 0;
    }

    // divisao
    case TK_Divisao: {
      token = le_token();
      if (F(F_p, F_c)) {
        geratemp(S1_hp);
        sprintf(S1_hc, "%s%s\t%s = %s / %s\n", S_hc, F_c, S1_hp, S_hp, F_p);
        if (S(S1_hp, S1_sp, S1_hc, S1_sc)) {
          strcpy(S_sp, S1_sp);
          strcpy(S_sc, S1_sc);
          return 1;
        } else {
          printf("DEBUG: Retornando 0 no S se divisao e F e !S\n");
        }
      } else {
        printf("DEBUG: Retornando 0 no S se divisao e !F\n");
      }
      return 0;
    }

    // resto da divisao (modulo)
    case TK_Resto: {
      token = le_token();
      if (F(F_p, F_c)) {
        geratemp(S1_hp);
        sprintf(S1_hc, "%s%s\t%s = %s mod %s\n", S_hc, F_c, S1_hp, S_hp, F_p);
        if (S(S1_hp, S1_sp, S1_hc, S1_sc)) {
          strcpy(S_sp, S1_sp);
          strcpy(S_sc, S1_sc);
          return 1;
        } else {
          printf("DEBUG: Retornando 0 no S se resto e F e !S\n");
        }
      } else {
        printf("DEBUG: Retornando 0 no S se resto e !F\n");
      }
      return 0;
    }
    /** fim aritmeticos */

    /************************************/
    /** Relacionais */
    // menor igual
    case TK_Menor_Igual: {
      token = le_token();
      if (F(F_p, F_c)) {
        geratemp(S1_hp);
        sprintf(S1_hc, "%s%s\t%s = %s <= %s\n", S_hc, F_c, S1_hp, S_hp, F_p);
        if (S(S1_hp, S1_sp, S1_hc, S1_sc)) {
          strcpy(S_sp, S1_sp);
          strcpy(S_sc, S1_sc);
          return 1;
        }
      }
      return 0;
    }

    // maior igual
    case TK_Maior_Igual: {
      token = le_token();
      if (F(F_p, F_c)) {
        geratemp(S1_hp);
        sprintf(S1_hc, "%s%s\t%s = %s >= %s\n", S_hc, F_c, S1_hp, S_hp, F_p);
        if (S(S1_hp, S1_sp, S1_hc, S1_sc)) {
          strcpy(S_sp, S1_sp);
          strcpy(S_sc, S1_sc);
          return 1;
        }
      }
      return 0;
    }

    // menor
    case TK_Menor: {
      token = le_token();
      if (F(F_p, F_c)) {
        geratemp(S1_hp);
        sprintf(S1_hc, "%s%s\t%s = %s < %s\n", S_hc, F_c, S1_hp, S_hp, F_p);
        if (S(S1_hp, S1_sp, S1_hc, S1_sc)) {
          strcpy(S_sp, S1_sp);
          strcpy(S_sc, S1_sc);
          return 1;
        }
      }
      return 0;
    }

    // maior
    case TK_Maior: {
      token = le_token();
      if (F(F_p, F_c)) {
        geratemp(S1_hp);
        sprintf(S1_hc, "%s%s\t%s = %s > %s\n", S_hc, F_c, S1_hp, S_hp, F_p);
        if (S(S1_hp, S1_sp, S1_hc, S1_sc)) {
          strcpy(S_sp, S1_sp);
          strcpy(S_sc, S1_sc);
          return 1;
        }
      }
      return 0;
    }

    // igual
    case TK_Igual: {
      token = le_token();
      if (F(F_p, F_c)) {
        geratemp(S1_hp);
        sprintf(S1_hc, "%s%s\t%s = %s == %s\n", S_hc, F_c, S1_hp, S_hp, F_p);
        if (S(S1_hp, S1_sp, S1_hc, S1_sc)) {
          strcpy(S_sp, S1_sp);
          strcpy(S_sc, S1_sc);
          return 1;
        }
      }
      return 0;
    }

    // diferente
    case TK_Diferente: {
      token = le_token();
      if (F(F_p, F_c)) {
        geratemp(S1_hp);
        sprintf(S1_hc, "%s%s\t%s = %s != %s\n", S_hc, F_c, S1_hp, S_hp, F_p);
        if (S(S1_hp, S1_sp, S1_hc, S1_sc)) {
          strcpy(S_sp, S1_sp);
          strcpy(S_sc, S1_sc);
          return 1;
        }
      }
      return 0;
    }
      /** fim relacionais */

    default: {
      strcpy(S_sp, S_hp);
      strcpy(S_sc, S_hc);
      return 1;
    }
  }
}

/* F -> id | cte | ( E ) */
int F(char F_p[MAX_COD], char F_c[MAX_COD]) {
  switch (token) {
    case TK_Const_Int: {
      geratemp(F_p);
      sprintf(F_c, "\t%s = %s\n", F_p, lex);
      token = le_token();
      return 1;
    }
    case TK_Abre_Par: {
      char E_c[MAX_COD], E_p[MAX_COD];
      token = le_token();
      if (E(E_p, E_c)) {
        if (token == TK_Fecha_Par) {
          token = le_token();
          strcpy(F_c, E_c);
          strcpy(F_p, E_p);
          return 1;
        } else {
          printf("Erro!!! Esperava fecha parenteses\n");
          printf("DEBUG: Retornando 0 no F se token == TK_Abre_Par e E e token != TK_Fecha_Par\n");
          return 0;
        }
      }
      printf("DEBUG: Retornando 0 no F se token == TK_Abre_Par e !E\n");
    }

    case TK_id:
    case TK_pv:
    case TK_int:
    case TK_float: {
      strcpy(F_c, "");
      strcpy(F_p, lex);
      token = le_token();
      return 1;
    }
    default: {
      printf("DEBUG: Retornando 0 no F se case default (token: %s)\n", tokens[token]);
      return 0;
    }
  }

  printf("DEBUG: Retornando 0 no F apos switch(token)");
  return 0;
}

int main() {
  FILE *arqout;
  char Com_C[MAX_COD];
  if ((arqin = fopen("arquivo.c", "rt")) == NULL) {
    printf("Erro na abertura do arquivo");
    exit(0);
  }
  if ((arqout = fopen("saida.kvmp", "wt")) == NULL) {
    printf("Erro na abertura do arquivo de saida");
    exit(0);
  }
  token = le_token();
  char Com_p[MAX_COD];
  while (token != TK_Fim_Arquivo) {
    if (token != TK_id) {
      // printf("DEBUG: Lido token %s\n", tokens[token]);
    }
    if (E(Com_p, Com_C) == 0) {
      printf("Erro no comando!!!\n");
      break;
    } else {
      fprintf(arqout, "%s", Com_C);
      printf("%s", Com_C);
    }
  }
  fclose(arqin);
  fclose(arqout);
}
