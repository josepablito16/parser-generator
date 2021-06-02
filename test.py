from tokenObj import *
from character import Character
import Produccion as p
import basic

cadena = '(.double result1=0,result2=0;.)Term<ref result1>{ "+"Term<ref result2> (.result1+=result2;.)| "-"Term<ref result2> (.result1-=result2;.)} (.result=result1;.).'

reservados = ['|', '(', ')', '{', '}', '[', ']']
textoPlano = cadena
pos = -1
charActual = None

TT_INT = 'INT'


def avanzar():
    '''
    Avanza una posicion en el textoPlano si no ha llegado al
    final del texto, caso contrario None
    '''
    global pos
    global textoPlano
    global charActual
    pos += 1
    if pos < len(textoPlano):
        charActual = textoPlano[pos]
    else:
        charActual = None


def explorar(salto=1):
    '''
    retorna el siguiente token si no ha llegado al final
    '''
    global pos
    global textoPlano
    global charActual

    if pos + salto < len(textoPlano) and pos + salto > 0:
        return textoPlano[pos + salto]
    else:
        return None


token = []
tokenAnonimo = ""
codigoTarget = ""
subProduccion = ""

# def identificar tokens
avanzar()
while charActual != None:
    #print(f'charActual = {charActual}')
    # caso 1
    # codigo target
    if (charActual == '(' and explorar() == '.'):

        if (len(subProduccion) > 0):
            # teniamos subproduccion anteriormente
            if subProduccion != " ":

                token.append(
                    Token(TT_INT, valor=p.Produccion(subProduccion), isSubProduccion=True))
            #print(f'subProduccion = {subProduccion}')
            subProduccion = ""

        # inicia codigo target
        avanzar()
        avanzar()
        codigoTarget += charActual
        avanzar()
        continue

    if (charActual == '.' and explorar() == ')'):
        # termina codigo target
        token.append(Token(TT_INT, valor=codigoTarget, isCodigoTarget=True))
        #print(f'codigoTarget = {codigoTarget}')
        avanzar()
        avanzar()
        codigoTarget = ""
        continue

    if (len(codigoTarget) > 0):
        # Estamos dentro de codigo target
        codigoTarget += charActual
        avanzar()
        continue

    # Caso 2
    # elementos reservados
    if (charActual in reservados):

        if (len(subProduccion) > 0):
            # teniamos subproduccion anteriormente
            if subProduccion != " ":
                token.append(
                    Token(TT_INT, valor=p.Produccion(subProduccion), isSubProduccion=True))
            #print(f'subProduccion = {subProduccion}')
            subProduccion = ""

        token.append(charActual)
        #print(f'charActual = {charActual}')
        avanzar()
        continue

    # Caso 3
    # Token anonimos
    if charActual == '"':

        if (len(subProduccion) > 0):
            # teniamos subproduccion anteriormente
            if subProduccion != " ":
                token.append(
                    Token(TT_INT, valor=p.Produccion(subProduccion), isSubProduccion=True))
            #print(f'subProduccion = {subProduccion}')
            subProduccion = ""
        if (len(tokenAnonimo) == 0):
            # es el inicio
            avanzar()
            tokenAnonimo += charActual
            avanzar()
            continue
        else:
            # es el final
            token.append(Token(TT_INT, Character(
                tokenAnonimo), isTokenAnonimo=True))
            #print(f'tokenAnonimo = {tokenAnonimo}')
            tokenAnonimo = ""
            avanzar()
            continue

    if (len(tokenAnonimo) > 0):
        # estamos en lectura de token anonimo
        tokenAnonimo += charActual
        avanzar()
        continue

    # caso 4
    # llamada a una produccion o subProduccion
    subProduccion += charActual
    avanzar()
    continue


for i in token:
    print(f'{i} es tipo {type(i)}')

basic.runProduccion(token)
