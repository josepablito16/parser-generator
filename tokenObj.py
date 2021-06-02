
class Token:
    '''
    Objeto que guarda el tipo y valor de cada token
    '''

    def __init__(self, tipo, valor=None, isTokenAnonimo=None, isSubProduccion=None, isCodigoTarget=None):
        self.tipo = tipo
        self.valor = valor
        self.isTokenAnonimo = isTokenAnonimo
        self.isSubProduccion = isSubProduccion
        self.isCodigoTarget = isCodigoTarget

    def getId(self):
        return f"{self.tipo}{self.valor}"

    def __repr__(self):
        if self.valor:
            return f'{self.tipo}:{self.valor}'
        return f'{self.tipo}'
