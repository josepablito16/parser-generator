
tokens = []


def Get():
	tokens.pop(0)


def Expect(elementos):
	if tokens[0]['tipo'] in elementos:
		Get()
	else:
		print(f'Error, se esperaba {elementos}')

# inicio de codigo dinamico 

        
def Expr(): 

	Stat ()
	Expect([';'])

def Stat(): 


	value = 0
	Expression(value)
	print(f"Resultado: {value}")

def Expression(result): 



	result1 = result2 = 0
	Term(result1)
	while (tokens[0]['tipo'] in ['-', '+']):
		if (tokens[0]['tipo'] in ['+']):

			Expect(['+'])
			Term(result2)
			result1 += result2
		if (tokens[0]['tipo'] in ['-']):

			Expect(['-'])
			Term(result2)
			result1 -= result2
	result = result1

def Term(result): 



	result1 = result2 = 0
	Factor(result1)
	while (tokens[0]['tipo'] in ['*', '/']):
		if (tokens[0]['tipo'] in ['*']):

			Expect(['*'])
			Factor(result2)
			result1 *= result2
		if (tokens[0]['tipo'] in ['/']):

			Expect(['/'])
			Factor(result2)
			result1 /= result2
	result = result1

def Factor(result): 

	sign = 1
	if (tokens[0]['tipo'] in ['-']):
		Expect(['-'])
		sign = -1

def Number(result): 

	number()
	decnumber()
	result = float(tokens[0]['valor'])
