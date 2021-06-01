
cadena = 'digit{digit}"."digit{digit}.'

for i in range(len(cadena) - 1, 0, -1):
    if(cadena[i] == '.'):
        print(i)
        break
