class Produccion:
    '''
    Objeto que toda la informacion de una produccion
    - No terminal
    - Atributo
    - Arbol de parseo
    '''

    def __init__(self, key, value):
        self.noTerminal = None
        self.atributo = None
        self.expresion = []
        self.arbol = None
        self.interpretarInformacion(key, value)

    def interpretarKey(self, key):
        if (key.fin('<') != -1):
            self.noTerminal = key[:key.find('<')].strip()
            self.atributo = key[key.find('<') + 1: key.find('>')].strip()
        else:
            self.noTerminal = key

    def interpretarValue(self, value):
        print(value)

    def interpretarInformacion(self, key, value):
        self.interpretarKey(key)
        self.interpretarValue(value)
