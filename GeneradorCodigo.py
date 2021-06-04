
contadorTab = 0
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
            codigoGenerado += f"{tabs}while ({Node.firstPos}):\n"
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
                codigoGenerado += f"{tabs}if ({Node.firstPos}):\n"
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
                codigoGenerado += f"{tabs}{Node.getValue().valor.noTerminal}({Node.getValue().valor.atributo})\n"
            elif (Node.getValue().isTokenAnonimo):
                tabs = "\t" * contadorTab
                codigoGenerado += f"{tabs}expect({Node.getValue().valor})\n"

        elif (Node.getValue().tipo in numeros):
            print("\nNUM2 ")
            print(Node.getValue().getInfo())
            if (Node.getValue().tipo == TT_ALFA):
                # Caso fin While
                contadorTab -= 1

    generarCodigo(Node.getLeft())
    generarCodigo(Node.getRight())
    print("-"*50)
    print(codigoGenerado)
