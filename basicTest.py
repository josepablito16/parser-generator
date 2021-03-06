import basic
from character import *
from tokenObj import *
# test = ['2+5*3', '2+2+2+2+2', '(1+2)/(1+2)', '123 123 123 +', '1+', '1 + d']


def getTest(texto):
    result, error = basic.run(texto)
    resultList = []
    for i in result:
        if (i.tipo == 'INT'):
            resultList.append(i.valor.elementos)
        else:
            resultList.append(i.tipo)

    if error:
        return str(error.asString())
    else:
        return resultList


'''
assert getTest([Character('a'), '|', Character('b'), '|', Character(
    'c')]) == "(({'a'}|{'b'})|{'c'})", "debería crear paréntesis"

# caso de concatencion 1
assert getTest(['(', Character('a'), '|', Character('b'), ')', Character(
    'c')]) == "(({'a'}|{'b'}).{'c'})", "debería crear concatenacion"

# caso de concatencion 3
assert getTest([Character('a'), Character('b'), '|', Character('c'), '|', Character('d'), Character(
    'e')]) == "((({'a'}.{'b'})|{'c'})|({'d'}.{'e'}))", "debería crear concatenacion y parentesis"

# CASO BRACKETS
assert getTest(['[', Character('a'), '|', Character('d'), ']', Character(
    'c')]) == "((({'a'}|{'d'})|E).{'c'})", "debería crear concatenacion y brackets"

# CASO BRACKETS unitario
assert getTest(['[', Character('a'), ']', Character(
    'c')]) == "(({'a'}|E).INT:{'c'})", "debería crear concatenacion y brackets"

# CASO BRACES
assert getTest(['{', Character('a'), '|', Character('d'), '}', Character(
    'c')]) == "((({'a'}|{'d'})*A).{'c'})", "debería crear concatenacion y braces"


# CASO BRACES unitario
assert getTest(['{', Character('a'), '}', Character(
    'c')]) == "(({'a'}*A).INT:{'c'})", "debería crear concatenacion y braces"

# CASO WHILE
assert getTest([Character('w'), Character('h'), Character('i'), Character('l'), Character(
    'e')]) == "(((({'w'}.{'h'}).{'i'}).{'l'}).{'e'})", "debería crear concatenacion WHILE"
'''
'''
lista = getTest([Character('L'),
                 '{', Character('L'), '|', Character('D'), '}'])
'''

# NUEVAS PRUEBAS PROYECTO 3

assert getTest(['{', Character('L'), '|', Character('D'), '}']
               ) == ['LPAREN', 'LPAREN', {'L'}, 'OR', {'D'}, 'RPAREN', 'MUL', 'ALFA', 'RPAREN']


assert getTest([Character('L'), '{', Character('L'), '|', Character('D'), '}']) == ['LPAREN', {
    'L'}, 'CONCAT', 'LPAREN', 'LPAREN', {'L'}, 'OR', {'D'}, 'RPAREN', 'MUL', 'ALFA', 'RPAREN', 'RPAREN']


assert getTest([Character('"'), Character('S'), '{', Character('S'), '}', Character('"')]) == ['LPAREN', 'LPAREN', 'LPAREN', {
    '"'}, 'CONCAT', {'S'}, 'RPAREN', 'CONCAT', 'LPAREN', {'S'}, 'MUL', 'ALFA', 'RPAREN', 'RPAREN', 'CONCAT', {'"'}, 'RPAREN']


assert getTest([Character('"'), '[', Character('/'), ']', Character('S'), Character('"')]) == ['LPAREN', 'LPAREN', 'LPAREN',
                                                                                               {'"'}, 'CONCAT', 'LPAREN', {'/'}, 'OR', 'EPSILON', 'RPAREN', 'RPAREN', 'CONCAT', {'S'}, 'RPAREN', 'CONCAT', {'"'}, 'RPAREN']
'''
print(getTest(['{', Character('L'), '|', Character('D'), '}']))
'''

print("TODO BIEN!")
