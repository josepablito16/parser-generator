from error import *
from tokenObj import *
from character import Character

#######################################
# CONSTANTES
#######################################

DIGITOS = list(map(chr, range(ord('0'), ord('9')+1))) + \
    ['.'] + list(map(chr, range(ord('a'), ord('z')+1)))


#######################################
# TOKENS
#######################################
# Constantes tokens tipos
TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_OR = 'OR'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_CONCAT = 'CONCAT'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_LBRACKET = 'LBRACKET'
TT_RBRACKET = 'RBRACKET'
TT_LBRACES = 'LBRACES'
TT_RBRACES = 'RBRACES'
TT_EPSILON = 'EPSILON'
TT_ALFA = 'ALFA'
TT_EOF = 'EOF'

# equivalente de cada token pero en simbolos
diccionario = {
    'PLUS': '+',
    'MINUS': '-',
    'MUL': '*',
    'DIV': '/',
    'OR': '|',
    'CONCAT': '.'
}

openTokens = ['(', '{', '[']
closeTokens = [')', '}', ']']

#######################################
# LEXER
#######################################


class Lexer:
    '''
    Encargado de asignar tokens a cada conjunto
    de caracteres identificado, caso contrario
    error
    '''

    def __init__(self, textoPlano):
        self.textoPlano = textoPlano
        self.pos = -1
        self.charActual = None
        self.avanzar()

    def avanzar(self):
        '''
        Avanza una posicion en el textoPlano si no ha llegado al
        final del texto, caso contrario None
        '''
        self.pos += 1
        if self.pos < len(self.textoPlano):
            self.charActual = self.textoPlano[self.pos]
        else:
            self.charActual = None

    def explorar(self, salto=1):
        '''
        retorna el siguiente token si no ha llegado al final
        '''

        if self.pos + salto < len(self.textoPlano) and self.pos + salto > 0:
            return self.textoPlano[self.pos + salto]
        else:
            return None

    def crearTokens(self):
        '''
        Crea una lista de tokens
        '''
        tokens = []

        # Mientras no haya llegado al final
        while self.charActual != None:

            if (isinstance(self.explorar(-1), Character) and isinstance(self.charActual, Character)):
                tokens.append(Token(TT_CONCAT))

            if (isinstance(self.charActual, Character) and isinstance(self.explorar(), Character)):
                tokens.append(Token(TT_INT, self.charActual))
                tokens.append(Token(TT_CONCAT))
                tokens.append(Token(TT_INT, self.explorar()))

                self.avanzar()
                self.avanzar()

            elif isinstance(self.charActual, Character):
                tokens.append(Token(TT_INT, self.charActual))
                try:
                    if (self.explorar() in "[{("):
                        tokens.append(Token(TT_CONCAT))
                except:
                    pass
                self.avanzar()

            # si es un espacio o tab solo avanza
            elif self.charActual in ' \t':
                self.avanzar()

                '''
				sino intenta reconocer el token y lo
				agrega a la lista tokens
				'''

            elif self.charActual == '+':
                tokens.append(Token(TT_PLUS))
                self.avanzar()
            elif self.charActual == '-':
                tokens.append(Token(TT_MINUS))
                self.avanzar()
            elif self.charActual == '|':
                tokens.append(Token(TT_OR))
                self.avanzar()
            elif self.charActual == '*':
                tokens.append(Token(TT_MUL))
                self.avanzar()
            elif self.charActual == '/':
                tokens.append(Token(TT_DIV))
                self.avanzar()
            elif self.charActual == '(':
                tokens.append(Token(TT_LPAREN))
                self.avanzar()
            elif self.charActual == ')':
                tokens.append(Token(TT_RPAREN))
                self.avanzar()
            elif self.charActual == '[':
                tokens.append(Token(TT_LBRACKET))
                self.avanzar()
            elif self.charActual == ']':
                tokens.append(Token(TT_RBRACKET))
                self.avanzar()
            elif self.charActual == '{':
                tokens.append(Token(TT_LBRACES))
                self.avanzar()
            elif self.charActual == '}':
                tokens.append(Token(TT_RBRACES))
                self.avanzar()
            else:
                # Retorna error si no reconoce el caracter
                char = self.charActual
                self.avanzar()
                return [], IllegalCharError(f"'{char}'")

        # al final agrega el token de final
        tokens.append(Token(TT_EOF))
        return tokens, None

    def crearTokens2(self):
        '''
        Crea una lista de tokens
        '''
        tokens = []
        if isinstance(self.textoPlano[0], Character):
            tokens.append(Token(TT_INT, self.textoPlano[0]))
        elif self.textoPlano[0] == '|':
            tokens.append(Token(TT_OR))
        elif self.textoPlano[0] == '(':
            tokens.append(Token(TT_LPAREN))
        elif self.textoPlano[0] == ')':
            tokens.append(Token(TT_RPAREN))
        elif self.textoPlano[0] == '[':
            tokens.append(Token(TT_LBRACKET))
        elif self.textoPlano[0] == ']':
            tokens.append(Token(TT_RBRACKET))
        elif self.textoPlano[0] == '{':
            tokens.append(Token(TT_LBRACES))
        elif self.textoPlano[0] == '}':
            tokens.append(Token(TT_RBRACES))

        # Mientras no haya llegado al final
        for index in range(1, len(self.textoPlano)):

            # caso 1
            # char . char
            if (isinstance(self.textoPlano[index-1], Character) and isinstance(self.textoPlano[index], Character)):
                tokens.append(Token(TT_CONCAT))
                tokens.append(Token(TT_INT, self.textoPlano[index]))

            # caso 2
            # char . open
            elif (isinstance(self.textoPlano[index-1], Character) and self.textoPlano[index] in openTokens):
                tokens.append(Token(TT_CONCAT))
                if self.textoPlano[index] == '(':
                    tokens.append(Token(TT_LPAREN))
                elif self.textoPlano[index] == '[':
                    tokens.append(Token(TT_LBRACKET))
                elif self.textoPlano[index] == '{':
                    tokens.append(Token(TT_LBRACES))

            # caso 3
            # close . char
            elif (self.textoPlano[index-1] in closeTokens and isinstance(self.textoPlano[index], Character)):
                tokens.append(Token(TT_CONCAT))
                tokens.append(Token(TT_INT, self.textoPlano[index]))

            else:
                if isinstance(self.textoPlano[index], Character):
                    tokens.append(Token(TT_INT, self.textoPlano[index]))
                elif self.textoPlano[index] == '|':
                    tokens.append(Token(TT_OR))
                elif self.textoPlano[index] == '(':
                    tokens.append(Token(TT_LPAREN))
                elif self.textoPlano[index] == ')':
                    tokens.append(Token(TT_RPAREN))
                elif self.textoPlano[index] == '[':
                    tokens.append(Token(TT_LBRACKET))
                elif self.textoPlano[index] == ']':
                    tokens.append(Token(TT_RBRACKET))
                elif self.textoPlano[index] == '{':
                    tokens.append(Token(TT_LBRACES))
                elif self.textoPlano[index] == '}':
                    tokens.append(Token(TT_RBRACES))
                else:
                    # Retorna error si no reconoce el caracter
                    char = self.textoPlano[index]
                    return [], IllegalCharError(f"'{char}'")

        # al final agrega el token de final
        tokens.append(Token(TT_EOF))
        return tokens, None

    def crearTokensProduccion(self):
        '''
        Crea una lista de tokens
        '''
        tokens = []
        if isinstance(self.textoPlano[0], Token):
            if (self.textoPlano[0].tipo == TT_INT):
                tokens.append(self.textoPlano[0])
        elif self.textoPlano[0] == '|':
            tokens.append(Token(TT_OR))
        elif self.textoPlano[0] == '(':
            tokens.append(Token(TT_LPAREN))
        elif self.textoPlano[0] == ')':
            tokens.append(Token(TT_RPAREN))
        elif self.textoPlano[0] == '[':
            tokens.append(Token(TT_LBRACKET))
        elif self.textoPlano[0] == ']':
            tokens.append(Token(TT_RBRACKET))
        elif self.textoPlano[0] == '{':
            tokens.append(Token(TT_LBRACES))
        elif self.textoPlano[0] == '}':
            tokens.append(Token(TT_RBRACES))

        # Mientras no haya llegado al final
        for index in range(1, len(self.textoPlano)):

            # caso 1
            # char . char
            try:
                if (self.textoPlano[index-1].tipo == self.textoPlano[index].tipo == TT_INT):
                    tokens.append(Token(TT_CONCAT))
                    tokens.append(self.textoPlano[index])
                    continue
            except:
                pass

            # caso 2
            # char . open
            try:
                if (self.textoPlano[index-1].tipo == TT_INT and self.textoPlano[index] in openTokens):
                    tokens.append(Token(TT_CONCAT))
                    if self.textoPlano[index] == '(':
                        tokens.append(Token(TT_LPAREN))
                    elif self.textoPlano[index] == '[':
                        tokens.append(Token(TT_LBRACKET))
                    elif self.textoPlano[index] == '{':
                        tokens.append(Token(TT_LBRACES))
                    continue
            except:
                pass

            # caso 3
            # close . char
            try:
                if (self.textoPlano[index-1] in closeTokens and self.textoPlano[index].tipo == TT_INT):
                    tokens.append(Token(TT_CONCAT))
                    tokens.append(self.textoPlano[index])
                    continue
            except:
                pass

            try:
                if self.textoPlano[index].tipo == TT_INT:
                    tokens.append(self.textoPlano[index])
                    continue
            except:
                pass
            if self.textoPlano[index] == '|':
                tokens.append(Token(TT_OR))
            elif self.textoPlano[index] == '(':
                tokens.append(Token(TT_LPAREN))
            elif self.textoPlano[index] == ')':
                tokens.append(Token(TT_RPAREN))
            elif self.textoPlano[index] == '[':
                tokens.append(Token(TT_LBRACKET))
            elif self.textoPlano[index] == ']':
                tokens.append(Token(TT_RBRACKET))
            elif self.textoPlano[index] == '{':
                tokens.append(Token(TT_LBRACES))
            elif self.textoPlano[index] == '}':
                tokens.append(Token(TT_RBRACES))
            else:
                # Retorna error si no reconoce el caracter
                char = self.textoPlano[index]
                return [], IllegalCharError(f"'{char}'")

        # al final agrega el token de final
        tokens.append(Token(TT_EOF))
        return tokens, None

    def crearNumero(self):
        numContact = ''
        contadorPuntos = 0

        '''
		Mientras no haya llegado al final del texto plano
		y el char actual sea numero o punto
		'''
        while self.charActual != None and self.charActual in DIGITOS:

            # Cuenta los puntos
            if self.charActual == '.':
                # Si ya hay un punto para
                if contadorPuntos == 1:
                    break
                contadorPuntos += 1
                numContact += '.'
            else:
                numContact += self.charActual
            self.avanzar()

        # decide si es un numero int o float
        if contadorPuntos == 0:
            return Token(TT_INT, int(numContact))
        else:
            return Token(TT_FLOAT, float(numContact))

#######################################
# NODES
#######################################


class NodoNumero:
    '''
    Nodo que solo contiene un numero
    '''

    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f'{self.token.valor}'


class NodoBinario:
    '''
    Nodo que contiene <nodo izquierdo> <operador> <nodo derecho>
    '''

    def __init__(self, nodoIzquierdo, tokenOperacion, nodoDerecho, agrupacion=None):
        self.nodoIzquierdo = nodoIzquierdo
        self.tokenOperacion = tokenOperacion
        self.nodoDerecho = nodoDerecho
        self.agrupacion = agrupacion
        self.listaTokens = []
        self.crearAgrupacion()

    def crearAgrupacion(self):
        #print(f"Nodo izquierdo = {self.nodoIzquierdo}")
        #print(f"Nodo operacion = {self.tokenOperacion}")
        #print(f"Nodo derecho = {self.nodoDerecho}")
        try:
            tipo = self.agrupacion.tipo
        except:
            tipo = None

        if (tipo in [TT_LPAREN, None]):
            self.listaTokens = [Token(
                TT_LPAREN), self.nodoIzquierdo, self.tokenOperacion, self.nodoDerecho, Token(TT_RPAREN)]

        elif (tipo == TT_LBRACKET):
            # OPCION
            self.listaTokens = [Token(TT_LPAREN), Token(TT_LPAREN), self.nodoIzquierdo, self.tokenOperacion, self.nodoDerecho, Token(
                TT_RPAREN), Token(TT_OR), Token(TT_EPSILON), Token(TT_RPAREN)]

        elif (tipo == TT_LBRACES):
            # 0 O MAS VECES
            self.listaTokens = [Token(TT_LPAREN), Token(TT_LPAREN), self.nodoIzquierdo, self.tokenOperacion, self.nodoDerecho, Token(
                TT_RPAREN), Token(TT_MUL), Token(TT_ALFA), Token(TT_RPAREN)]

    def __repr__(self):
        try:
            tipo = self.agrupacion.tipo
        except:
            tipo = None

        if (tipo in [TT_LPAREN, None]):
            return f"({self.nodoIzquierdo}{diccionario[self.tokenOperacion.tipo]}{self.nodoDerecho})"

        elif (tipo == TT_LBRACKET):
            # return f"[{self.nodoIzquierdo}{diccionario[self.tokenOperacion.tipo]}{self.nodoDerecho}]"
            return f"(({self.nodoIzquierdo}{diccionario[self.tokenOperacion.tipo]}{self.nodoDerecho})|E)"

        elif (tipo == TT_LBRACES):
            # return f"{chr(123)}{self.nodoIzquierdo}{diccionario[self.tokenOperacion.tipo]}{self.nodoDerecho}{chr(125)}"
            return f"(({self.nodoIzquierdo}{diccionario[self.tokenOperacion.tipo]}{self.nodoDerecho})*A)"


class NodoUnitario:
    '''
    Nodo que contiene <nodo izquierdo> <operador> <nodo derecho>
    '''

    def __init__(self, nodo, agrupacion=None):
        self.nodo = nodo
        self.agrupacion = agrupacion
        self.listaTokens = []
        self.crearAgrupacion()

    def crearAgrupacion(self):
        try:
            tipo = self.agrupacion.tipo
        except:
            tipo = None

        if (tipo in [TT_LPAREN, None]):
            self.listaTokens = [
                Token(TT_LPAREN), self.nodo, Token(TT_RPAREN)]

        elif (tipo == TT_LBRACKET):
            # OPCION
            '''
            self.listaTokens = [
                Token(TT_LBRACKET), self.nodo, Token(TT_RBRACKET)]
            '''
            self.listaTokens = [Token(TT_LPAREN), self.nodo, Token(
                TT_OR), Token(TT_EPSILON), Token(TT_RPAREN)]

        elif (tipo == TT_LBRACES):
            # 0 O MAS VECES
            '''
            self.listaTokens = [
                Token(TT_LBRACES), self.nodo, Token(TT_RBRACES)]
            '''
            self.listaTokens = [Token(TT_LPAREN), self.nodo, Token(
                TT_MUL), Token(TT_ALFA), Token(TT_RPAREN)]

    def __repr__(self):
        try:
            tipo = self.agrupacion.tipo
        except:
            tipo = None

        if (tipo in [TT_LPAREN, None]):
            return f"({self.nodo.valor})"

        elif (tipo == TT_LBRACKET):
            return f"({self.nodo.valor}|E)"

        elif (tipo == TT_LBRACES):
            return f"({self.nodo.valor}*A)"

#######################################
# PARSER DE RESULTADOS
#######################################


class ParseResultados:
    '''
    Lleva el control de errores o avances del parser
    '''

    def __init__(self):
        self.error = None
        self.nodo = None

    def registrar(self, res):
        '''
        Registra una operacion nueva del parser,
        actualiza errores de ser necesario
        '''
        if isinstance(res, ParseResultados):
            if res.error:
                self.error = res.error
            return res.nodo
        return res

    def success(self, nodo):
        '''
        Marca como exitoso una operacion del parser
        '''
        self.nodo = nodo
        return self

    def failure(self, error):
        '''
        Marca como fallida una operacion del parser
        '''
        self.error = error
        return self

#######################################
# PARSER
#######################################


class Parser:
    '''
    Convierte una secuencia de tokens en una estructura
    de datos, crea parentesis donde sea necesario y retorna
    una cadena con los parentesis apropiados para armar el arbol
    '''

    def __init__(self, tokens):
        self.tokens = tokens
        self.tokenId = -1
        self.tokenGrupo = None
        self.avanzar()

    def avanzar(self):
        '''
        Pasamo a la siguiente posicion si no hemos
        llegado al final
        '''
        self.tokenId += 1
        if self.tokenId < len(self.tokens):
            self.tokenActual = self.tokens[self.tokenId]
        return self.tokenActual

    def makeSymbol(self):
        token = self.tokenActual
        if (token.tipo == TT_LPAREN):
            self.avanzar()
            res = self.expr()

            if (self.tokenActual.tipo != TT_RPAREN):
                print("Error : se esperaba )")
            self.avanzar()
            return res

        elif (token.tipo == TT_INT):
            self.avanzar()
            return token

    def makeGroup(self):
        res = self.makeSymbol()

        '''
            Mientras no hayamos llegado al final y encuentre { o [
        '''
        while (self.tokenActual.tipo != TT_EOF and (self.tokenActual.tipo == TT_LBRACES or self.tokenActual.tipo == TT_LBRACKET)):

            if (self.tokenActual.tipo == TT_LBRACES):
                self.avanzar()

                res = NodoBinario(self.expr(), Token(TT_MUL),
                                  Token(TT_ALFA))

                if (self.tokenActual.tipo != TT_RBRACES):
                    print("Error: se esperaba }")
                self.avanzar()

            elif(self.tokenActual.tipo == TT_LBRACKET):
                self.avanzar()

                res = NodoBinario(self.expr(), Token(TT_OR), Token(TT_EPSILON))

                if (self.tokenActual.tipo != TT_RBRACKET):
                    print('Error: se esperaba ]')
                self.avanzar()
        return res

    def term(self):
        res = self.makeGroup()

        '''
            Mientras no hayamos llegado al final y tengamos concatenacion
        '''
        while (self.tokenActual.tipo != TT_EOF and self.tokenActual.tipo == TT_CONCAT):
            self.avanzar()
            res = NodoBinario(res, Token(TT_CONCAT), self.makeGroup())

        return res

    def expr(self):
        res = self.term()

        while self.tokenActual.tipo != TT_EOF and self.tokenActual.tipo == TT_OR:
            self.avanzar()
            res = NodoBinario(res, Token(TT_OR), self.expr())

        return res

    def parse(self):
        res = self.expr()
        return res

#######################################
# RUN
#######################################


def getSubListaNodes(root):
    listaSubNodos = []

    if(isinstance(root, NodoBinario)):
        for j in root.listaTokens:
            if(isinstance(j, NodoBinario)):
                listaSubNodos += getSubListaNodes(j)
            else:
                listaSubNodos.append(j)

    return listaSubNodos


def getListNodes(root):
    '''
    self.nodoIzquierdo = nodoIzquierdo
                                                                                                                                    self.tokenOperacion = tokenOperacion
                                                                                                                                    self.nodoDerecho = nodoDerecho
    '''
    listaNodos = []
    if isinstance(root, NodoBinario):
        for i in root.listaTokens:
            if(isinstance(i, NodoBinario)):
                listaNodos += getSubListaNodes(i)
            else:
                listaNodos.append(i)
    else:
        pass
        # print(root)

    # esto se tiene que retornar
    return listaNodos


def run(textoPlano):
    '''
    Metodo principal que llama al lexer y al parser
    '''
    # print()
    # print(textoPlano)
    lexer = Lexer(textoPlano)
    tokens, error = lexer.crearTokens2()
    #print(f'\nTOKENS \n {tokens}\n')
    if error:
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()
    # print()
    return getListNodes(ast), None


def runProduccion(textoPlano):
    '''
    Metodo principal que llama al lexer y al parser
    '''
    # print()
    # print(textoPlano)
    lexer = Lexer(textoPlano)
    tokens, error = lexer.crearTokensProduccion()
    #print(f'\nTOKENS \n {tokens}\n')

    if error:
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()
    #print(f'\Tokens final \n {getListNodes(ast)}\n')
    return getListNodes(ast)
