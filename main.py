import re #regular expressions

class Token:
	def __init__(self, ttype, tvalue):
		self.ttype = ttype
		self.tvalue = tvalue

class Tokenizer:
	def __init__(self, origin):
		self.origin = origin
		self.position = 0
		self.current = self.selectNext()

	def selectNext(self): #updates position
		c = "" #input placeholder | previously a number, troublemaker that made me sad and literally caused V1.0.3

	#mini-rework compared to V1.2 and previous versions
		while (self.position<(len(self.origin)) and (self.origin[self.position]).isspace()): #for white spaces
			self.position += 1
		
		if self.position == len(self.origin): #this means we got to the end of the input and we'll have to add something there
			token = Token(END,"END")
			self.current = token
			c = "END"

		while (self.position<(len(self.origin)) and (self.origin[self.position]).isdigit()): #we'll be good till we find a symbol/reach the end of inp
			c += self.origin[self.position] #stores the number
			self.position += 1

		if c == "END":
			return

	#end of mini-rework (delete this comment on the next version)

		elif c == "":
			if self.origin[self.position] == "+": #we're about to sum something!
				token = Token(PLUS, "+") 
				self.position += 1
				self.current = token
				
			elif self.origin[self.position] == "-": #we're about to subtract something!
				token = Token(MINUS, "-") 
				self.position += 1
				self.current = token

			elif self.origin[self.position] == "*": #we're about to multiply something!
				token = Token(MULT, "*") 
				self.position += 1
				self.current = token

			elif self.origin[self.position] == "/": #we're about to divide something!
				token = Token(DIV, "/") 
				self.position += 1
				self.current = token

			elif self.origin[self.position] == '(': #we're about to give priority to something!
				token = Token(POPN, "(")
				self.position += 1
				self.current = token
			
			elif self.origin[self.position] == ')': #we're about to end someone's priority!
				token = Token(PCLS, ")")
				self.position += 1
				self.current = token
	
			else:
				raise Exception("Token not found")
		else:
			
			c = int(c)
			token = Token(INT, c)
			self.current = token

		return token



class Parser: #token parser

	def run(stg):
		proCode = PrePro.filter(stg)
		Parser.token = Tokenizer(stg) #let the fun begin
		#print(Parser.token.current.ttype)	
		tree = Parser.parserExpression() #Raul is our Lord and Savior
		if Parser.token.current.ttype == END: #praise Raul!
			return tree
		else:
			raise Exception("Error - Unexpected token")

	def parserFactor():
		if Parser.token.current.ttype == INT:
			total = IntVal(Parser.token.current.tvalue, [])
			Parser.token.selectNext()

		elif Parser.token.current.ttype == POPN:
			Parser.token.selectNext()
			total = Parser.parserExpression()
			if Parser.token.current.ttype == PCLS:
				Parser.token.selectNext()
			else:
				raise Exception("Error - missing parenthesis )")

		elif Parser.token.current.ttype == PLUS: 
			Parser.token.selectNext()
			children = [Parser.parserFactor()]
			total = UnOp("+", children)

		elif Parser.token.current.ttype == MINUS:
			Parser.token.selectNext()
			children = [Parser.parserFactor()]
			total = UnOp("-", children)

		else:
			raise Exception("Error - unidentified token")

		return total

	def parserTerm():
		total = Parser.parserFactor()
		while Parser.token.current.ttype == MULT or Parser.token.current.ttype == DIV:
			if Parser.token.current.ttype == MULT: 
				Parser.token.selectNext()
				children = [total, Parser.parserFactor()]
				total = BinOp("*", children)

			if Parser.token.current.ttype == DIV:
				Parser.token.selectNext()
				children = [total, Parser.parserFactor()]
				total = BinOp("/", children)
		
		return total

	@staticmethod
	def parserExpression():
		total = Parser.parserTerm() #priority 
		while Parser.token.current.ttype == PLUS or Parser.token.current.ttype == MINUS: 
			if Parser.token.current.ttype == PLUS: 
				Parser.token.selectNext()
				children = [total, Parser.parserTerm()] #literally took me an hour to find this self-copy paste bug
				total = BinOp("+", children)

			if Parser.token.current.ttype == MINUS:
				Parser.token.selectNext()
				children = [total, Parser.parserTerm()] #literally took me an hour to find this self-copy paste bug
				total = BinOp("-", children)

		return total



class PrePro:
	def filter(inp_stg):
		print("Input = " + inp_stg)
		return re.sub("'.*\n","", inp_stg) #replace substrings module

class Node:
	def __init__(self):
		self.value = None
		self.children = []

	def Evaluate(self):
		pass

class BinOp(Node): #binary ops -> a(binop)b = c
	def __init__(self, val, child):
		self.value = val
		self.children = child

	def Evaluate(self):
		if self.value == "+":
			return self.children[0].Evaluate() + self.children[1].Evaluate()
		elif self.value == "-":
			return self.children[0].Evaluate() - self.children[1].Evaluate()
		elif self.value == "*":
			return self.children[0].Evaluate() * self.children[1].Evaluate()
		elif self.value == "/":
			return self.children[0].Evaluate() / self.children[1].Evaluate()

class UnOp(Node): #unary ops -> -(a) = -a | -(-a) = a
	def __init__(self, val, child):
		self.value = val
		self.children = child
	
	def Evaluate(self):
		if self.value == "-":
			return -(self.children[0].Evaluate())
		else:
			return self.children[0].Evaluate()

class IntVal(Node): #gets and returns int
	def __init__(self, val, child):
		self.value = val
		self.children = child	
	
	def Evaluate(self):
		return self.value

class NoOp(Node): #dummy - nothing to do here yet
	def __init__(self, val, child):
		self.value = val
		self.children = child	

	def Evaluate(self):
		return

#Tokens
PLUS = "PLUS" #sum 
MINUS = "MINUS" #subtract | negative numbers
INT = "INT" #digits (currently ints only)
END = "END" #end of input
MULT = "MULT" #multiply
DIV = "DIV" #divide	
POPN = "(" #parenthesis open
PCLS = ")"	#parenthesis close

def main():
	with open("inputs.vbs", "r") as inVals:
		inpFile = inVals.readlines()

	i = 0
	while i < len(inpFile): #iterating through every line from input file (it calculates aswell, duh)
		try:
			print("\n"+"----- Line "+str(i)+" -----")
			inpFile[i] = inpFile[i].replace("\\n", "\n") #previously this removed spaces and that's not good 
			out = Parser.run(inpFile[i])
			print("Result = "+str(out.Evaluate()))
			i += 1
		except Exception as err:
			i += 1
			print(err)

if __name__== "__main__":
    main()	
