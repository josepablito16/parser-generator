import GeneradorCodigo as gc


class Produccion:
    '''
    Objeto que toda la informacion de una produccion
    - No terminal
    - Atributo
    - Arbol de parseo
    '''

    def __init__(self, key, value=None, filename=None):
        self.noTerminal = None
        self.atributo = None
        self.expresion = []
        self.arbol = None
        self.interpretarInformacion(key, value, filename)

    def interpretarKey(self, key):
        if (key.find('<') != -1):
            self.noTerminal = key[:key.find('<')].strip()
            self.atributo = key[key.find('<') + 1: key.find('>')].strip()
        else:
            self.noTerminal = key

    def interpretarValue(self, value, filename):
        f = open(filename, "a+")
        if (self.atributo != None):
            f.write(f"def {self.noTerminal}({self.atributo}): \n")
        else:
            f.write(f"def {self.noTerminal}(): \n")
        f.close()
        gc.procesarProduccion(value, filename)
        # print(value)

    def interpretarInformacion(self, key, value, filename):
        self.interpretarKey(key)
        if (value != None):
            self.interpretarValue(value, filename)

    def __repr__(self):
        return f'no terminal = {self.noTerminal}; atributo = {self.atributo}'
