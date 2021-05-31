open = ['(', '{', '[']
close = [')', '}', ']']
char = ['"', 'S']

entrada = ['"', 'S', '{', 'S', '}', '"']

salida = []
salida.append(entrada[0])
for index in range(1, len(entrada)):
    print(f'{entrada[index-1]} {entrada[index]}')
    if (entrada[index-1] in char and entrada[index] in char):
        salida.append(".")
        salida.append(entrada[index])

    elif (entrada[index-1] in char and entrada[index] in open):
        salida.append(".")
        salida.append(entrada[index])

    elif (entrada[index-1] in close and entrada[index] in char):
        salida.append(".")
        salida.append(entrada[index])

    else:
        salida.append(entrada[index])

print(salida)
