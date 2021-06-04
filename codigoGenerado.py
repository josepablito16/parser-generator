codigo inicial
esto ya deberia de estar
def Expr(): 

	Stat ()
	expect([';'])
def Stat(): 


	value = 0
	Expression(value)
	print(f"Resultado: {value}")
def Expression(result): 



	result1 = result2 = 0
	Term(result1)
	while (['-', '+']):
		if (['+']):

			expect(['+'])
			Term(result2)
			result1 += result2
		if (['-']):

			expect(['-'])
			Term(result2)
			result1 -= result2
	result = result1
def Term(result): 



	result1 = result2 = 0
	Factor(result1)
	while (['/', '*']):
		if (['*']):

			expect(['*'])
			Factor(result2)
			result1 *= result2
		if (['/']):

			expect(['/'])
			Factor(result2)
			result1 /= result2
	result = result1
def Factor(result): 

	sign = 1
	if (['-']):
		expect(['-'])
		sign = -1
def Number(result): 

	number()
	decnumber()
	result = float(self.prev_token.value)
