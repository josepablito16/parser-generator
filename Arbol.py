from Nodo import Node
from itertools import product
import Directo as d

import basic
from character import *
from tokenObj import *

TT_OR = 'OR'
TT_MUL = 'MUL'
TT_CONCAT = 'CONCAT'

TT_INT = 'INT'
TT_EPSILON = 'EPSILON'
TT_ALFA = 'ALFA'

TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'

TT_HASHTAG = 'HASHTAG'


class Arbol(object):
    """
    El objeto Arbol contiene metodos utiles
    para construir un arbol y recorrerlo.

    Variable
    ----------
    pila : list
        guarda la cola de objetos antes de
        llegar a un operador y construir los
        nodos del arbol
    operadores : list
        Operadores aceptados por el programa
    numeros : list
        Contiene todos los simbolos aceptados por
        el programa

    """

    def __init__(self):
        self.pila = []
        self.operadores = [TT_OR, TT_MUL, TT_CONCAT]
        self.numeros = [TT_EPSILON, TT_ALFA, TT_HASHTAG]
        self.diccionario = {}

    def postOrder(self, Node):
        '''
        Recorre el arbol de forma postoperden
        y va construyendo los NFA usando el 
        algoritmo de Thompson

        Parametros
        ----------
        Node: Obj Node
            Nodo raiz del arbol

        '''
        # Si no existe raiz no seguimos
        if(Node == None):
            return

        # Ejecutamos postOrden en los nodos hijos
        self.postOrder(Node.getLeft())
        self.postOrder(Node.getRight())

        if(Node.getValue() in self.operadores):

            # Si el nodo actual es un Operadores
            if(Node.getValue() == TT_OR):
                N1 = self.pila[len(self.pila)-1]
                N2 = self.pila[len(self.pila)-2]

                self.pila.pop()
                self.pila.pop()

                # print(f"({N2}|{N1})")
                # print('-'*50)
                #print(f'{N2} tipo {type(N2)}')
                # print('OR')
                #print(f'{N1} tipo {type(N1)}')
                # print('-'*50)

                self.pila.append(f"({N2}|{N1})")

            if(Node.getValue() == TT_MUL):
                N1 = self.pila[len(self.pila)-1]
                N2 = self.pila[len(self.pila)-2]

                self.pila.pop()
                self.pila.pop()

                # print(f"({N2}*{N1})")
                # print('-'*50)
                #print(f'{N2} tipo {type(N2)}')
                # print('*')
                #print(f'{N1} tipo {type(N1)}')
                # print('-'*50)

                self.pila.append(f"({N2}*{N1})")

            if(Node.getValue() == TT_CONCAT):
                N1 = self.pila[len(self.pila)-1]
                N2 = self.pila[len(self.pila)-2]

                self.pila.pop()
                self.pila.pop()

                # print(f"({N2}.{N1})")
                # print('-'*50)
                #print(f'{N2} tipo {type(N2)}')
                # print('CONCAT')
                #print(f'{N1} tipo {type(N1)}')
                # print('-'*50)
                self.pila.append(f"({N2}.{N1})")

        else:
            # Si el nodo actual no es un operador
            self.pila.append(Node.getValue())

    def armarArbol(self, entrada):
        '''
        Recorre la expr aumentada y 
        arma el arbol para el algoritmo directo

        Parametros
        ----------
        entrada: str
            Expr ingresada

        Returns
        ----------
            Nodo raiz


        '''
        root = Node(None)
        actual = root

        # Se arma el arbol
        for i in entrada:

            if (isinstance(i, Token)):
                # es parentesis, operador Alfa o Beta

                if(i.tipo == TT_LPAREN):
                    # Se crea nodo izquiedo
                    # Se mueve al nodo izquierdo
                    actual.setLeft(None, actual)
                    actual = actual.getLeft()

                if(i.tipo in self.operadores):
                    # Se pone el valor al nodo: {i}
                    # Se crea nodo derecho
                    # Se mueve al nodo derecho
                    actual.setValue(i.tipo)
                    actual.setRight(None, actual)
                    actual = actual.getRight()

                if(i.tipo == TT_RPAREN):
                    # Se mueve a la raiz del nodo
                    actual = actual.getRoot()

                if(i.tipo in self.numeros):
                    # Se pone el valor al nodo: {i}
                    # Se mueve a la raiz del nodo
                    # Token <'ALFA'> o <'EPSILON'> o <'HASHTAG'>
                    actual.setValue(i)
                    actual = actual.getRoot()

                if(i.tipo == TT_INT):
                    # Sabemos que es <Char>

                    # Se pone el valor al nodo: {i}
                    # Se mueve a la raiz del nodo
                    actual.setValue(i.valor)  # <Character>
                    actual = actual.getRoot()

            elif (isinstance(i, basic.NodoNumero)):
                # Sabemos que es <Char>

                # Se pone el valor al nodo: {i}
                # Se mueve a la raiz del nodo
                actual.setValue(i.token.valor)  # <Character>
                actual = actual.getRoot()

        return root

    def armarArbolProduccion(self, entrada):
        '''
        Recorre la expr aumentada y 
        arma el arbol para el algoritmo directo

        Parametros
        ----------
        entrada: str
            Expr ingresada

        Returns
        ----------
            Nodo raiz


        '''
        root = Node(None)
        actual = root

        #print('Se arma el arbol')
        for i in entrada:

            if (isinstance(i, Token)):
                # es parentesis, operador Alfa o Beta

                if(i.tipo == TT_LPAREN):
                    #print('Se crea nodo izquiedo')
                    #print('Se mueve al nodo izquierdo')
                    actual.setLeft(None, actual)
                    actual = actual.getLeft()

                if(i.tipo in self.operadores):
                    #print(f'Se pone el valor al nodo: {i}')
                    #print('Se crea nodo derecho')
                    #print('Se mueve al nodo derecho')
                    actual.setValue(i)
                    actual.setRight(None, actual)
                    actual = actual.getRight()

                if(i.tipo == TT_RPAREN):
                    #print('Se mueve a la raiz del nodo')
                    actual = actual.getRoot()

                if(i.tipo in self.numeros):
                    #print(f'Se pone el valor al nodo: {i}')
                    #print('Se mueve a la raiz del nodo')
                    # Token <'ALFA'> o <'EPSILON'> o <'HASHTAG'>
                    actual.setValue(i)
                    actual = actual.getRoot()

                if(i.tipo == TT_INT):
                    # Sabemos que es <Char>

                    #print(f'Se pone el valor al nodo: {i}')
                    #print('Se mueve a la raiz del nodo')
                    actual.setValue(i)  # <Character>
                    actual = actual.getRoot()

            elif (isinstance(i, basic.NodoNumero)):
                # Sabemos que es <Char>

                #print(f'Se pone el valor al nodo: {i}')
                #print('Se mueve a la raiz del nodo')
                actual.setValue(i.token.valor)  # <Character>
                actual = actual.getRoot()

        return root
