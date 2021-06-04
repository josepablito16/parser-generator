from tokenObj import *
from character import Character
import Produccion as p
import basic
from Arbol import *
# --------------------
contadorTab = 1
codigoGenerado = ""
ifAbierto = False

TT_INT = 'INT'

TT_OR = 'OR'
TT_MUL = 'MUL'
TT_CONCAT = 'CONCAT'

TT_EPSILON = 'EPSILON'
TT_ALFA = 'ALFA'
TT_HASHTAG = 'HASHTAG'

numeros = [TT_EPSILON, TT_ALFA, TT_HASHTAG]
operadores = [TT_OR, TT_MUL, TT_CONCAT]

# ----------------------
reservados = ['|', '(', ')', '{', '}', '[', ']']
textoPlano = ""
pos = -1
charActual = None
token = []


def generarCodigo(Node):
    '''
    Recorre el arbol postOrden para calcular
    nullable, firstpos y lastPos
    '''
    global contadorTab
    global codigoGenerado
    global ifAbierto

    if(Node == None):
        return

    # print()
    # print(Node.getValue())
    # print(type(Node.getValue()))
    #print(f'{Node.getValue()} tipo {type(Node.getValue())}')
    if(Node.getValue().tipo in operadores):
        # Operadores
        if(Node.getValue().tipo == TT_OR):
            print("\nOR")
            print(Node.getValue().getInfo())

        if(Node.getValue().tipo == TT_MUL):
            # Caso while
            print("\nMUL")
            print(Node.getValue().getInfo())
            tabs = "\t" * contadorTab
            codigoGenerado += f"{tabs}while (tokens[0]['tipo'] in {Node.firstPos}):\n"
            contadorTab += 1

        if(Node.getValue().tipo == TT_CONCAT):
            # Caso concat
            print("\nCONCAT")
            print(Node.getValue().getInfo())

            # Revisa si el padre del nodo es un Or
            try:
                isPadreOr = Node.getRoot().getValue().tipo == TT_OR
                print("CONCAT con padre OR")
            except:
                isPadreOr = False

            if (isPadreOr):
                if(ifAbierto):
                    contadorTab -= 1
                    ifAbierto = False
                else:
                    ifAbierto = True

                tabs = "\t" * contadorTab
                codigoGenerado += f"{tabs}if (tokens[0]['tipo'] in {Node.firstPos}):\n"
                contadorTab += 1
            else:
                codigoGenerado += "\n"

    else:
        if (Node.getValue().tipo == TT_INT):
            print("\nNUM1")
            print(Node.getValue().getInfo())

            if (Node.getValue().isCodigoTarget):
                # Es codigo target
                tabs = "\t" * contadorTab
                codigoGenerado += f"{tabs}{Node.getValue().valor}\n"

            elif (Node.getValue().isSubProduccion):
                # Es subexpresion
                tabs = "\t" * contadorTab
                atributo = Node.getValue().valor.atributo
                if (atributo != None):
                    codigoGenerado += f"{tabs}{Node.getValue().valor.noTerminal}({atributo})\n"
                else:
                    codigoGenerado += f"{tabs}{Node.getValue().valor.noTerminal}()\n"

            elif (Node.getValue().isTokenAnonimo):
                tabs = "\t" * contadorTab
                codigoGenerado += f'{tabs}Expect({list(Node.getValue().valor.elementos)})\n'

        elif (Node.getValue().tipo in numeros):
            print("\nNUM2 ")
            print(Node.getValue().getInfo())
            if (Node.getValue().tipo == TT_ALFA):
                # Caso fin While
                contadorTab -= 2

    generarCodigo(Node.getLeft())
    generarCodigo(Node.getRight())
    print("-"*50)
    print(codigoGenerado)


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


def identificarTokens():
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
            token.append(
                Token(TT_INT, valor=codigoTarget, isCodigoTarget=True))
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


def procesarProduccion(produccionPlana, filename):
    global textoPlano
    global contadorTab
    global ifAbierto
    global pos
    global charActual
    global token
    global codigoGenerado

    contadorTab = 1
    codigoGenerado = ""
    ifAbierto = False
    textoPlano = ""
    pos = -1
    charActual = None
    token = []
    textoPlano = produccionPlana

    identificarTokens()
    for i in token:
        print(f'{i} es tipo {type(i)}')

    produccionFinal = basic.runProduccion(token)

    a = Arbol()
    arbol = a.armarArbolProduccion(produccionFinal)

    print("Calcular primera")
    calcularPrimeraPos(arbol)
    print('\nGeneracion de codigo')
    generarCodigo(arbol)

    f = open(filename, "a+")
    f.write(codigoGenerado)
    f.close()


if __name__ == "__main__":
    cadena = '(.double result1=0,result2=0;.)Term<ref result1>{ "+"Term<ref result2> (.result1+=result2;.)| "-"Term<ref result2> (.result1-=result2;.)} (.result=result1;.).'
    procesarProduccion(cadena, "codigoGenerado.py")
