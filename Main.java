package exp_operaores3;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.RandomAccessFile;

public class Main {
	final int TK_int = 1;
	final int TK_float = 2;
	final int TK_char = 3;
	final int TK_struct = 4;
	final int TK_if = 5;
	final int TK_else = 6;

	final int TK_id = 7;
	final int TK_Abre_Colch = 8;
	final int TK_Fecha_Colch = 9;
	final int TK_Abre_Chaves = 10;
	final int TK_Fecha_Chaves = 11;
	final int TK_Fim_Arquivo = 12;
	final int TK_Atrib = 13;
	final int TK_Const_Int = 14;
	final int TK_Mais = 15;
	final int TK_Menos = 16;
	final int TK_Mult = 17;
	final int TK_Abre_Par = 18;
	final int TK_Fecha_Par = 19;
	final int TK_virgula = 20;
	final int TK_pv = 21;
	final int TK_Maior = 22;
	final int TK_Menor = 23;
	final int TK_Menor_Igual = 24;
	final int TK_Maior_Igual = 25;
	final int TK_Igual = 26;
	final int TK_Diferente = 27;
	final int TK_while = 28;
	final int TK_and_bitwise = 29;
	final int TK_and_logico = 30;
	final int TK_Div = 31;
	final int TK_Rest_Div = 32;
	final int TK_Mais_Ig = 33;
	final int TK_Menos_Ig = 34;

	RandomAccessFile arquivo;

	String[] tokens = { "", "TK_int", "TK_float", "TK_char", "TK_struct", "TK_if", "TK_else", "TK_id", "TK_Abre_Colch",
			"TK_Fecha_Colch", "TK_Abre_Chaves", "TK_Fecha_Chaves", "TK_Fim_Arquivo", "TK_Atrib", "TK_Const_Int",
			"TK_Mais", "TK_Menos", "TK_Mult", "TK_Abre_Par", "TK_Fecha_Par", "TK_virgula", "TK_pv", "TK_Maior",
			"TK_Menor", "TK_Menor_Igual", "TK_Maior_Igual", "TK_Igual", "TK_Diferente", "TK_Divisão",
			"TK_Resto_Divisão", "TK_Mais_Igual", "TK_Menos_Igual" };

	int token;
	static int proxposTS = 0;
	String lex = "";
	int linlex = 0, collex = 1;
	Palavra[] reservadas = { new Palavra("int", TK_int), new Palavra("float", TK_float), new Palavra("char", TK_char),
			new Palavra("struct", TK_struct), new Palavra("if", TK_if), new Palavra("else", TK_else),
			new Palavra("while", TK_while), new Palavra("fim", -1) };

	int numlabel = 0;
	int numtemp = 0;
	
	boolean flagL = false;
	
	final int MAX_COD = 1000;
	// RESTAURA
	int tokenant;
	long posarq;
	String lexant;
	char ccant;
	int marcou = 0;

	public void marca_pos() throws IOException {
		marcou = 1;
		tokenant = token;
		posarq = arquivo.getFilePointer();
		lexant = lex;
	}

	public void restaura() throws IOException {
		arquivo.seek(posarq);
		token = tokenant;
		lex = lexant;
	}

	public static void main(String[] args) throws IOException {
		Main m = new Main();
		m.le_arquivo();
		m.init();
	}

	public void init() throws IOException {

		token = le_token();
		String com_C = "", com_p = "";
		// while(token != TK_Fim_Arquivo) {
		String r = E(com_p, com_C);

		if (r != null) {
			com_p = r.split("¨")[0];
			com_C = r.split("¨")[1];

			for (String s : com_p.split("   ")) {
				System.out.println(s);
			}

			System.out.println("Resposta armazenada em: " + com_C);

			// System.out.println(com_p);
		} else {
			System.out.println("ERRO");
		}
		// }
	}

	public void le_arquivo() throws IOException {

		arquivo = new RandomAccessFile("./arqc.c", "rw");
		System.out.println(arquivo.length());
		arquivo.seek(0);
	}

	public char le_char() throws IOException {
		if (arquivo.getFilePointer() == arquivo.length()) {
			return '~';
		}
		char c = (char) arquivo.readByte();

		if (c != -1) {
			if (c == '\n' || c == '\r') {
				linlex++;
				collex = 1;
			} else {
				collex++;
			}
			return (char) c;
		} else {
			return '~';
		}

	}

	public int pal_res(String lex) {
		int tk = 0;
		while (reservadas[tk].getPalavra().compareTo("fim") != 0) {
			if (lex.compareTo(reservadas[tk].getPalavra()) == 0) {
				return reservadas[tk].getTk();
			}
			tk++;
		}
		return TK_id;
	}

	public int le_token() throws IOException {
		int pos = 0;
		int estado = 0;
		char c = '\0';
		while (true) {
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
						return TK_Mais_Ig;
					}
					return TK_Mais;
				}
				if (c == '-') {
					c = le_char();
					if (c == '=') {
						c = le_char();
						return TK_Menos_Ig;
					}
					return TK_Menos;
				}
				if (c == '/') {
					c = le_char();
					return TK_Div;
				}
				if (c == '%') {
					c = le_char();
					return TK_Rest_Div;
				}
				if (c == '*') {
					c = le_char();
					return TK_Mult;
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
					lex = ";";
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
						flagL = true;
						return TK_Igual;
					}
					lex = "=";
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
				if (c == '&') {
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
				if (c >= 'a' && c <= 'z' || c >= 'A' && c <= 'Z' || c == '_') {
					lex = "";
					lex = lex + (char) c;
					c = le_char();
					pos = 1;
					estado = 1;
					break;
				}
				if (c >= '0' && c <= '9') {
					lex = "";
					lex = lex + (char) c;
					c = le_char();
					pos = 1;
					estado = 2;
					break;
				}
				if (c == '~')
					return TK_Fim_Arquivo;
				if (c == '\n' || c == '\r' || c == '\t' || c == '\0' || c == ' ') {
					c = le_char();
					break;
				}
			case 1:
				if (c >= 'a' && c <= 'z' || c >= 'A' && c <= 'Z' || c == '_' || c >= '0' && c <= '9') {
					lex = lex + (char) c;
					c = le_char();
					break;
				} else {
					estado = 0;
					return pal_res(lex);
				}
			case 2:
				if (c >= '0' && c <= '9') {
					lex = lex + (char) c;
					c = le_char();
					break;
				} else {
					estado = 0;
					return TK_Const_Int;
				}
			}
		}
	}

	public void mostra_t() {
		System.out.println(tokens[token] + "lex = " + lex + linlex + " " + collex);
	}

	public String geralabel(String label) {
		return label + "LB00" + numlabel++;
	}

	public String geratemp(String temp) {
		return temp + "T00" + numtemp++;
	}

	public String A(String A_p, String A_c) throws IOException {
		String A1_p = "", A1_c = "", E_p = "", E_c = "";
		String id;
		String r = E(E_p, E_c);
		if (r.split("¨").length > 0)
			E_p = r.split("¨")[0];
		if (r.split("¨").length > 1)
			E_c = r.split("¨")[1];
		if (r == null)
			return null;

		if (token != TK_Atrib) {
			A_p = E_p;
			A_c = E_c;
			return A_p + "¨" + A_c;
		}
		token = le_token(); // consome o sinal de atribui��o
		r = A(A1_p, A1_c);
		if (r == null)
			return null;
		if (r.split("¨").length > 0)
			A1_p = r.split("¨")[0];
		if (r.split("¨").length > 1)
			A1_c = r.split("¨")[1];

		A_c = A_c + A1_c + "   " + E_p + "=" + A1_p;
		A_p = E_p;

		return A_p + "¨" + A_c;
	}

	public String Rel(String Rel_c, String Rel_true, String Rel_false) throws IOException {

		String E1_c = "", E2_c = "", R_sc = "", E1_p = "", E2_p = "", R_sp = "";

		String r = E(E1_p, E1_c);
		if (r != null) {
			if (r.split("¨").length > 0)
				E1_p = r.split("¨")[0];
			if (r.split("¨").length > 1)
				E1_c = r.split("¨")[1];

			String op = null;
			if (token == TK_Maior)
				op = op + ">";
			else if (token == TK_Menor)
				op = op + "<";
			else if (token == TK_Igual)
				op = op + "=";
			else if (token == TK_Diferente)
				op = op + "<>";
			else if (token == TK_Maior_Igual)
				op = op + ">=";
			else if (token == TK_Menor_Igual)
				op = op + "<=";
			if (token == TK_Maior || token == TK_Menor || token == TK_Igual || token == TK_Diferente
					|| token == TK_Maior_Igual || token == TK_Menor_Igual) {
				token = le_token();
				r = E(E2_p, E2_c);
				if (r != null) {
					if (r.split("¨").length > 0)
						E2_p = r.split("¨")[0];
					if (r.split("¨").length > 1)
						E2_c = r.split("¨")[1];
					Rel_c = Rel_c + E1_c + E2_c + "   " + E1_p + " " + op + " " + E2_p + "goto " + Rel_true + "\n "
							+ "goto" + Rel_false;
					return Rel_c;
				}
				return null;
			} else
				return null;
		}
		return null;

	}

	public String E(String E_p, String E_c) throws IOException {
		String T_p = "", T_c = "", R_hp = "", R_sp = "", R_hc = "", R_sc = "", Q_hp = "", Q_sp = "", Q_hc = "",
				Q_sc = "", L_hp = "", L_sp = "", L_hc = "", L_sc = "";
		String r = T(T_p, T_c);
		if (r != null) {
			if (r.split("¨").length > 0)
				T_p = r.split("¨")[0];
			if (r.split("¨").length > 1)
				T_c = r.split("¨")[1];

			R_hc = T_c;
			R_hp = T_p;

			r = R(R_hp, R_sp, R_hc, R_sc);

			if (r != null) {
				if (r.split("¨").length > 0)
					R_sc = r.split("¨")[0];
				if (r.split("¨").length > 1)
					R_sp = r.split("¨")[1];

				L_hc = R_sc;
				L_hp = R_sp;

				r = L(L_hp, L_sp, L_hc, L_sc);

				if (r != null) {
					if (r.split("¨").length > 0)
						L_sc = r.split("¨")[0];
					if (r.split("¨").length > 1)
						L_sp = r.split("¨")[1];

					Q_hc = L_sc;
					Q_hp = L_sp;

					r = Q(Q_hp, Q_sp, Q_hc, Q_sc);
					if (r != null) {
						if (r.split("¨").length > 0)
							Q_sc = r.split("¨")[0];
						if (r.split("¨").length > 1)
							Q_sp = r.split("¨")[1];

						E_c = Q_sc;
						E_p = Q_sp;

						return E_p + "¨" + E_c;
					}
				}
			}
		}
		return null;
	}

	public String Q(String R_hp, String R_sp, String R_hc, String R_sc) throws IOException {
		String T_c = "", R1_hc = "", R1_sc = "", T_p = "", R1_hp = "", R1_sp = "";

		if (token == TK_Atrib) {
			token = le_token();
			String r = A(T_p, T_c);
			if (r != null) {
				if (r.split("¨").length > 0)
					T_p = r.split("¨")[0];
				if (r.split("¨").length > 1)
					T_c = r.split("¨")[1];

				R1_hp = geratemp(R1_hp);
				// R1_hc = R1_hc + R_hc + T_c + " " + R1_hp + "=" + R_hp + T_p;
				R1_hc = R1_hc + R1_hp + "=" + R_hc + T_c + "   " + R1_hp + "=" + R_hp + T_p + "\n";
				r = R(R1_hp, R1_sp, R1_hc, R1_sc);
				if (r != null) {
					if (r.split("¨").length > 0)
						R_sp = r.split("¨")[0];
					if (r.split("¨").length > 1)
						R_sc = r.split("¨")[1];
					return R_sp + "¨" + R_sc;
				}
			}
		}
		if (token == TK_Mais_Ig) {
			token = le_token();
			String r = A(T_p, T_c);
			if (r != null) {
				if (r.split("¨").length > 0)
					T_p = r.split("¨")[0];
				if (r.split("¨").length > 1)
					T_c = r.split("¨")[1];

				R1_hp = geratemp(R1_hp);
				// R1_hc = R1_hc + R_hc + T_c + " " + R1_hp + "=" + R_hp + T_p;
				R1_hc = R1_hc + R1_hp + "=" + R_hc + R_hp + T_p + R1_hp + "=" + R1_hp + "+" + R_hc + T_c + "\n";
				r = R(R1_hp, R1_sp, R1_hc, R1_sc);
				if (r != null) {
					if (r.split("¨").length > 0)
						R_sp = r.split("¨")[0];
					if (r.split("¨").length > 1)
						R_sc = r.split("¨")[1];
					return R_sp + "¨" + R_sc;
				}
			}
		}
		if (token == TK_Menos_Ig) {
			token = le_token();
			String r = A(T_p, T_c);
			if (r != null) {
				if (r.split("¨").length > 0)
					T_p = r.split("¨")[0];
				if (r.split("¨").length > 1)
					T_c = r.split("¨")[1];

				R1_hp = geratemp(R1_hp);
				// R1_hc = R1_hc + R_hc + T_c + " " + R1_hp + "=" + R_hp + T_p;
				R1_hc = R1_hc + R1_hp + "=" + R_hc + R_hp + T_p + R1_hp + "=" + R1_hp + "-" + R_hc + T_c + "\n";
				r = R(R1_hp, R1_sp, R1_hc, R1_sc);
				if (r != null) {
					if (r.split("¨").length > 0)
						R_sp = r.split("¨")[0];
					if (r.split("¨").length > 1)
						R_sc = r.split("¨")[1];
					return R_sp + "¨" + R_sc;
				}
			}
		}
		R_sp = R_hp;
		R_sc = R_hc;
		return R_sp + "¨" + R_sc;
	}

	public String L(String R_hp, String R_sp, String R_hc, String R_sc) throws IOException {
		String T_c = "", R1_hc = "", R1_sc = "", T_p = "", R1_hp = "", R1_sp = "";

		if (token == TK_Igual) {
			token = le_token();
			String r = T(T_p, T_c);
			if (r != null) {
				if (r.split("¨").length > 0)
					T_p = r.split("¨")[0];
				if (r.split("¨").length > 1)
					T_c = r.split("¨")[1];

				R1_hp = geratemp(R1_hp);
				R1_hc = R1_hc + R_hp  + T_c + "   " + R1_hp + "=" + R_hc + "==" + T_p + "\n";
				r = R(R1_hp, R1_sp, R1_hc, R1_sc);
				if (r != null) {
					if (r.split("¨").length > 0)
						R_sp = r.split("¨")[0];
					if (r.split("¨").length > 1)
						R_sc = r.split("¨")[1];
					
					if(flagL)
					return R_sc + "¨" + R_sp;
					else
					return R_sp + "¨" + R_sc;
	
				}
			}
			return null;
		}
		R_sp = R_hp;
		R_sc = R_hc;
		return R_sp + "¨" + R_sc;
	}

	public String R(String R_hp, String R_sp, String R_hc, String R_sc) throws IOException {
		String T_c = "", R1_hc = "", R1_sc = "", T_p = "", R1_hp = "", R1_sp = "";

		if (token == TK_Mais) {
			token = le_token();
			String r = T(T_p, T_c);
			if (r != null) {
				if (r.split("¨").length > 0)
					T_p = r.split("¨")[0];
				if (r.split("¨").length > 1)
					T_c = r.split("¨")[1];

				R1_hp = geratemp(R1_hp);
				R1_hc = R1_hc + R_hc + T_c + "   " + R1_hp + "=" + R_hp + "+" + T_p + "\n";
				r = R(R1_hp, R1_sp, R1_hc, R1_sc);
				if (r != null) {
					if (r.split("¨").length > 0)
						R_sp = r.split("¨")[0];
					if (r.split("¨").length > 1)
						R_sc = r.split("¨")[1];

					return R_sp + "¨" + R_sc;
				}
			}
			return null;
		}
		if (token == TK_Menos) {
			token = le_token();
			String r = T(T_p, T_c);
			if (r != null) {
				if (r.split("¨").length > 0)
					T_p = r.split("¨")[0];
				if (r.split("¨").length > 1)
					T_c = r.split("¨")[1];

				R1_hp = geratemp(R1_hp);
				R1_hc = R1_hc + R_hc + T_c + "   " + R1_hp + "=" + R_hp + "-" + T_p + "\n";
				r = R(R1_hp, R1_sp, R1_hc, R1_sc);
				if (r != null) {
					if (r.split("¨").length > 0)
						R_sp = r.split("¨")[0];
					if (r.split("¨").length > 1)
						R_sc = r.split("¨")[1];
					return R_sp + "¨" + R_sc;
				}
			}
			return null;
		}
		R_sp = R_hp;
		R_sc = R_hc;
		return R_sp + "¨" + R_sc;
	}

	public String T(String T_p, String T_c) throws IOException {
		String F_c = "", F_p = "", S_hp = "", S_sp = "", S_hc = "", S_sc = "";

		String r = F(F_p, F_c);
		if (r != null) {
			if (r.split("¨").length > 0)
				F_p = r.split("¨")[0];
			if (r.split("¨").length > 1)
				F_c = r.split("¨")[1];

			S_hc = F_c;
			S_hp = F_p;

			r = S(S_hp, S_sp, S_hc, S_sc);
			if (r != null) {
				if (r.split("¨").length > 1)
					T_c = r.split("¨")[1];
				if (r.split("¨").length > 0)
					T_p = r.split("¨")[0];

				return T_p + "¨" + T_c;
			}
		}
		return null;
	}

	public String S(String S_hp, String S_sp, String S_hc, String S_sc) throws IOException {
		String F_c = "", S1_hc = "", S1_sc = "", F_p = "", S1_hp = "", S1_sp = "";
		if (token == TK_Mult) {
			token = le_token();
			String r = F(F_p, F_c);
			if (r != null) {
				if (r.split("¨").length > 0)
					F_p = r.split("¨")[0];
				if (r.split("¨").length > 1)
					F_c = r.split("¨")[1];
				S1_hp = geratemp(S1_hp);

				S1_hc = S1_hc + S_hc + F_c + "   " + S1_hp + "=" + S_hp + "*" + F_p;
				r = S(S1_hp, S1_sp, S1_hc, S1_sc);
				if (r != null) {
					if (r.split("¨").length > 0)
						S_sp = r.split("¨")[0];
					if (r.split("¨").length > 1)
						S_sc = r.split("¨")[1];
					return S_sp + "¨" + S_sc;
				}
			}
			return null;
		}
		if (token == TK_Div) {
			token = le_token();
			String r = F(F_p, F_c);
			if (r != null) {
				if (r.split("¨").length > 0)
					F_p = r.split("¨")[0];
				if (r.split("¨").length > 1)
					F_c = r.split("¨")[1];
				S1_hp = geratemp(S1_hp);

				S1_hc = S1_hc + S_hc + F_c + "   " + S1_hp + "=" + S_hp + "/" + F_p;
				r = S(S1_hp, S1_sp, S1_hc, S1_sc);
				if (r != null) {
					if (r.split("¨").length > 0)
						S_sp = r.split("¨")[0];
					if (r.split("¨").length > 1)
						S_sc = r.split("¨")[1];
					return S_sp + "¨" + S_sc;
				}
			}
			return null;
		}
		if (token == TK_Rest_Div) {
			token = le_token();
			String r = F(F_p, F_c);
			if (r != null) {
				if (r.split("¨").length > 0)
					F_p = r.split("¨")[0];
				if (r.split("¨").length > 1)
					F_c = r.split("¨")[1];
				S1_hp = geratemp(S1_hp);

				S1_hc = S1_hc + S_hc + F_c + "   " + S1_hp + "=" + S_hp + "%" + F_p;
				r = S(S1_hp, S1_sp, S1_hc, S1_sc);
				if (r != null) {
					if (r.split("¨").length > 0)
						S_sp = r.split("¨")[0];
					if (r.split("¨").length > 1)
						S_sc = r.split("¨")[1];
					return S_sp + "¨" + S_sc;
				}
			}
			return null;
		}
		S_sp = S_hp;
		S_sc = S_hc;
		return S_sp + "¨" + S_sc;
	}

	public String F(String F_p, String F_c) throws IOException {

		if (token == TK_Const_Int) {
			F_p = geratemp(F_p);
			F_c = F_c + "   " + F_p + " = " + lex;
			token = le_token();

			return F_p + "¨" + F_c;
		}
		if (token == TK_id) {
			F_c = "";
			F_p = lex;
			token = le_token();
			return F_p + "¨" + F_c;
		}
		if (token == TK_Abre_Par) {
			String E_c = null, E_p = null;
			token = le_token();
			String r = E(E_p, E_c);
			if (r != null) {
				E_p = r.split("¨")[0];
				E_c = r.split("¨")[1];
				if (token == TK_Fecha_Par) {
					token = le_token();
					F_c = E_c;
					F_p = E_p;

					return F_p + "¨" + F_c;
				} else {
					System.out.println("Erro!!! Esperava fecha parenteses\n");
					return null;
				}
			}
		}

		return null;
	}

	// COMANDOS

}
