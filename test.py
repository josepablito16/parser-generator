from tokenObj import *
from character import Character
import Produccion as p
import basic
from Arbol import *

cadena = '(.double result1=0,result2=0;.)Term<ref result1>{ "+"Term<ref result2> (.result1+=result2;.)| "-"Term<ref result2> (.result1-=result2;.)} (.result=result1;.).'

reservados = ['|', '(', ')', '{', '}', '[', ']']
textoPlano = cadena
pos = -1
charActual = None

TT_INT = 'INT'

TT_OR = 'OR'
TT_MUL = 'MUL'
TT_CONCAT = 'CONCAT'

TT_EPSILON = 'EPSILON'
TT_ALFA = 'ALFA'
TT_HASHTAG = 'HASHTAG'

numeros = [TT_EPSILON, TT_ALFA, TT_HASHTAG]
operadores = [TT_OR, TT_MUL, TT_CONCAT]


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

produccionFinal = basic.runProduccion(token)

#print('Produccion final')
# print(produccionFinal)

a = Arbol()
arbol = a.armarArbolProduccion(produccionFinal)

# print("PostOrden")
# a.postOrder(arbol)


def union(lista):
    '''
    Quita elementos repetidos de una lista
    '''
    return list(set(lista))


def calcularNullableOr(nodo):
    nodo.setNullable(nodo.getLeft().isNullable()
                     or nodo.getRight().isNullable())


def calcularFirstLastPosOr(nodo):
    nodo.addFirstPos(
        union(
            nodo.getLeft().getFirstPos()
            +
            nodo.getRight().getFirstPos()
        )
    )


def calcularNullableHoja(nodo):
    print('Nullable')
    print(nodo.getValue())
    print(type(nodo.getValue().tipo))
    if (isinstance(nodo.getValue(), Token)):
        if(nodo.getValue().tipo == TT_EPSILON):
            nodo.setNullable(True)
        else:
            nodo.setNullable(False)


def calcularFirstLastPosHoja(nodo):
    print('First Pos')
    print(nodo.getValue())
    if (isinstance(nodo.getValue(), Token)):
        if (isinstance(nodo.getValue().valor, Character)):
            print(f'first pos = {list(nodo.getValue().valor.elementos)[0]}')
            nodo.addFirstPos(list(nodo.getValue().valor.elementos)[0])


def calcularNullableConcat(nodo):
    nodo.setNullable(nodo.getLeft().isNullable()
                     and nodo.getRight().isNullable())


def calcularFirstLastPosConcat(nodo):
    if (nodo.getLeft().isNullable()):
        nodo.addFirstPos(
            union(
                nodo.getLeft().getFirstPos()
                +
                nodo.getRight().getFirstPos()
            )
        )
    else:
        nodo.addFirstPos(
            nodo.getLeft().getFirstPos()
        )


def calcularNullableStar(nodo):
    nodo.setNullable(True)


def calcularFirstLastPosStar(nodo):
    nodo.addFirstPos(
        nodo.getLeft().getFirstPos()
    )


def calcularPrimeraPos(Node):
    '''
    Recorre el arbol postOrden para calcular
    nullable, firstpos y lastPos
    '''
    if(Node == None):
        return

    calcularPrimeraPos(Node.getLeft())
    calcularPrimeraPos(Node.getRight())

    # print()
    # print(Node.getValue())
    # print(type(Node.getValue()))
    #print(f'{Node.getValue()} tipo {type(Node.getValue())}')
    if(Node.getValue().tipo in operadores):
        # Operadores
        if(Node.getValue().tipo == TT_OR):
            print("\nOR")
            calcularNullableOr(Node)
            calcularFirstLastPosOr(Node)

        if(Node.getValue().tipo == TT_MUL):
            print("\nMUL")
            calcularNullableStar(Node)
            calcularFirstLastPosStar(Node)

        if(Node.getValue().tipo == TT_CONCAT):
            print("\nCONCAT")
            calcularNullableConcat(Node)
            calcularFirstLastPosConcat(Node)

    else:
        if (Node.getValue().tipo == TT_INT):
            print("\nNUM1")
            calcularFirstLastPosHoja(Node)
            calcularNullableHoja(Node)

        elif (Node.getValue().tipo in numeros):
            print("\nNUM2 ")
            calcularFirstLastPosHoja(Node)
            calcularNullableHoja(Node)


print("Calcular primera")
calcularPrimeraPos(arbol)
print('importante')
print(arbol.getLeft().getRight().getFirstPos())
