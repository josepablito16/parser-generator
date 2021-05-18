class Character:
    def __init__(self, elementos):
        self.elementos = set(elementos)

    def getId(self):
        ordenado = sorted(self.elementos)
        return ''.join(ordenado)

    def __repr__(self):
        # return f"{self.elementos}"
        return f"<Character> {self.getId()}"

    def union(self, character):
        self.elementos = self.elementos.union(set(character))

    def diferencia(self, character):
        self.elementos = self.elementos.difference(set(character))

    def getObj(self):
        return self
