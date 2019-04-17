import re #regular expressions
import sys

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

		while (self.position<(len(self.origin)) and (self.origin[self.position]).isspace() and self.origin[self.position] != "\n"): #for white spaces
			self.position += 1
			
		if self.position == len(self.origin): #this means we got to the end of the input and we'll have to add something there
			token = Token(EOF,"EOF")
			self.current = token
			c = "EOF"
			return token #return added

		if self.origin[self.position] == "\n": #checks if we reached the end of a line
			token = Token(BREAK,"\n") #this caused "string out of range"
			self.position += 1
			self.current = token
			return token

		while (self.position<(len(self.origin)) and (self.origin[self.position]).isdigit()): #we'll be good till we find a symbol/reach the end of inp
			c += self.origin[self.position] #stores the number
			self.position += 1

		if c == "":
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

			elif self.origin[self.position] == '=': #we're about assign something
				token = Token(ASGN, "=")
				self.position += 1
				self.current = token

			elif self.origin[self.position] == '<': #we're about assign something
				token = Token(LSST, "<")
				self.position += 1
				self.current = token

			elif self.origin[self.position] == '>': #we're about assign something
				token = Token(GRTT, ">")
				self.position += 1
				self.current = token

			elif self.origin[self.position].isalpha(): #then Raul said: "python users will be blessed with .isalpha()"
				idntT = ""
				while (self.position<(len(self.origin)) and (self.origin[self.position]).isdigit() or 
				self.origin[self.position] == "_" or self.origin[self.position].isalpha()): #we'll be good till we find a symbol/reach the end of inp
					idntT += self.origin[self.position]
					self.position += 1
				
				temp = idntT.upper()

				if temp in RWL:
					token = Token(temp, temp) #previously with an identifier - caused a funny error (not really, I cried)
					self.current = token
				else:
					token = Token(IDNT, temp)
					self.current = token
	
			else:
				raise Exception("Token not found " + str(self.origin[self.position]))

		else:
			c = int(c)
			token = Token(INT, c)
			self.current = token

		return token



class Parser: #token parser

	def run(stg):
		proCode = PrePro.filter(stg)
		Parser.token = Tokenizer(proCode) #previously missed something here
		tree = Parser.parserStatements() 
		Parser.token.selectNext()
		while Parser.token.current.ttype == BREAK:
			Parser.token.selectNext()
		if Parser.token.current.ttype == EOF: #praise Raul!
			return tree
		else:
			raise Exception("Error - Unexpected token "+str(Parser.token.current.ttype))

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

		elif Parser.token.current.ttype == IDNT:
			total = Identifier(Parser.token.current.tvalue, [])
			Parser.token.selectNext()

		elif Parser.token.current.ttype == INPT:
			total = InputOp([])
			Parser.token.selectNext()

		else:
			raise Exception("Error - unidentified token - " + str(Parser.token.current.tvalue))

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

	def parserRelExpression():
		total = Parser.parserExpression() #priority 
		if Parser.token.current.ttype == GRTT: #greater than
			Parser.token.selectNext()
			children = [total, Parser.parserExpression()]
			total = BinOp(">", children)

		if Parser.token.current.ttype == LSST: #less than
			Parser.token.selectNext()
			children = [total, Parser.parserExpression()]
			total = BinOp("<", children)

		if Parser.token.current.ttype == "=":
			Parser.token.selectNext()
			children = [total, Parser.parserExpression()]
			total = BinOp("=", children)

		return total

	def parserStatements():
		statementList = [Parser.parserStatement()]
		while Parser.token.current.ttype == BREAK:
			Parser.token.selectNext()
			statementList.append(Parser.parserStatement())

		return Statements("statements", statementList)

	def parserStatement():
		if Parser.token.current.ttype == IDNT:
			ident = Parser.token.current.tvalue
			Parser.token.selectNext()

			if Parser.token.current.ttype == ASGN:
				assign = Parser.token.current.tvalue
				Parser.token.selectNext()
				total = Assignment(assign, [ident, Parser.parserExpression()])
			else:
				raise Exception("Error - Assignment '=' expecte	d")
		
		elif Parser.token.current.ttype == "PRINT":
			Parser.token.selectNext()
			total = Print("PRINT", [Parser.parserExpression()])
		
		elif Parser.token.current.ttype == WHILE:
			Parser.token.selectNext()
			total = WhileOp("while", [Parser.parserRelExpression()])

			if Parser.token.current.ttype == BREAK:
				Parser.token.selectNext()
				total.children.append(Parser.parserStatements())

			if Parser.token.current.ttype != WEND:
				raise Exception("Error - 'WEND' expected")
			Parser.token.selectNext()

		elif Parser.token.current.ttype == IF:
			Parser.token.selectNext()
			total = IfOp([Parser.parserRelExpression()])
			if Parser.token.current.ttype == THEN:
				Parser.token.selectNext()

				if Parser.token.current.ttype == BREAK:
					Parser.token.selectNext()	
					total.children.append(Parser.parserStatements())

					if Parser.token.current.ttype == ELSE:
						Parser.token.selectNext()

						if Parser.token.current.ttype == BREAK:
							Parser.token.selectNext()
							total.children.append(Parser.parserStatements())
			
					if Parser.token.current.ttype != END:
						raise Exception("Error - 'END (IF)' expected")
					Parser.token.selectNext()

					if Parser.token.current.ttype != IF:
						raise Exception("Error - 'IF' expected")
					Parser.token.selectNext()
		else:
			total = NoOp(0,[])
		
		return total


class PrePro:
	def filter(inp_stg):
		#print("Input = " + inp_stg)
		return re.sub("'.*\n","", inp_stg) #replace substrings module

class Node:
	def __init__(self):
		self.value = None
		self.children = []

	def Evaluate(self):
		pass

class BinOp(Node): #binary ops -> a(binop)b = c
	def __init__(self, value, children):
		self.value = value
		self.children = children

	def Evaluate(self,symb):
		if self.value == "+":
			return self.children[0].Evaluate(symb) + self.children[1].Evaluate(symb)
		elif self.value == "-":
			return self.children[0].Evaluate(symb) - self.children[1].Evaluate(symb)
		elif self.value == "*":
			return self.children[0].Evaluate(symb) * self.children[1].Evaluate(symb)
		elif self.value == "/":
			return self.children[0].Evaluate(symb) / self.children[1].Evaluate(symb)
		elif self.value == "=":
			return self.children[0].Evaluate(symb) == self.children[1].Evaluate(symb)
		elif self.value == "<":
			return self.children[0].Evaluate(symb) < self.children[1].Evaluate(symb)
		elif self.value == ">":
			return self.children[0].Evaluate(symb) > self.children[1].Evaluate(symb)

class UnOp(Node): #unary ops -> -(a) = -a | -(-a) = a
	def __init__(self, value, children):
		self.value = value
		self.children = children
	
	def Evaluate(self, symb): #I forgot to add symb there aaaaaaaaaaaaaaaaaaaaa
		if self.value == "-":
			return -(self.children[0].Evaluate(symb))
		else:
			return self.children[0].Evaluate(symb)

class IntVal(Node): #gets and returns int
	def __init__(self, value, children): 
		self.value = value
		self.children = children	
	
	def Evaluate(self, symb): #I forgot to add symb there aaaaaaaaaaaaaaaaaaaaa
		return self.value

class NoOp(Node): #dummy - nothing to do here
	def __init__(self, value, children):
		self.value = value
		self.children = children	

	def Evaluate(self,symb):
		return

class Assignment(Node): #sets value to given variable - a = K
	def __init__(self, value, children):
		self.value = value
		self.children = children
	
	def Evaluate(self, symb):
		return symb.setter(self.children[0], self.children[1].Evaluate(symb))


class Identifier(Node):
	def __init__(self, value, children):
		self.value = value
		self.children = children
	
	def Evaluate(self, symb):
		return symb.getter(self.value)

class Statements(Node): #statement in statements
	def __init__(self, value, children):
		self.value = value
		self.children = children
	
	def Evaluate(self, symb):
		for i in self.children:
			#idk why this doesn't work... I don't know what to do anymore
			i.Evaluate(symb)

class Print(Node): 
	def __init__(self, value, children):
		self.value = value
		self.children = children
	
	def Evaluate(self,symb):
		print(self.children[0].Evaluate(symb))

class WhileOp(Node):
	def __init__(self, value, children):
		self.value = value
		self.children = children

	def Evaluate(self,symb):
		while self.children[0].Evaluate(symb):
			self.children[1].Evaluate(symb)

class IfOp(Node):
	def __init__(self, children):
		self.children = children
	
	def Evaluate(self,symb):
		if self.children[0].Evaluate(symb):
			return self.children[1].Evaluate(symb)
		else:
			if len(self.children) == 3:
				return self.children[2].Evaluate(symb)
			else:
				pass

class InputOp(Node):
	def __init__(self, value,children):
		self.value = value
		self.children = children
	
	def Evaluate(self,symb):
		return int(input(""))

class SymbolTable:
	def __init__(self):
		self.varDict = {}

	def getter(self, var): #returns value for variable
		if var in self.varDict.keys():
			return self.varDict[var]
		else:
			raise Exception("Error - undefined variable")

	def setter(self, var, value): #assigns value to variable
		self.varDict[var] = value


#Tokens
PLUS = "PLUS" #sum 
MINUS = "MINUS" #subtract | negative numbers
INT = "INT" #digits (currently ints only)
EOF = "EOF" #end of input
MULT = "MULT" #multiply
DIV = "DIV" #divide	
POPN = "(" #parenthesis open
PCLS = ")"	#parenthesis close

ASGN = "=" #assignment
BREAK = "\n" #line break
IDNT = "IDENTIFIER" #identifier, O RLY?
GRTT = ">" #greater than
LSST = "<" #less than
INPT = "INPUT" #input
WHILE = "WHILE" #while start
WEND = "WEND" #while end 
IF = "IF" #if token
THEN = "THEN" #then token
END = "END"
ELSE = "ELSE"
 

#reserved words list
RWL = ["BEGIN", "END", "PRINT", "IF", "THEN","ELSE", "OR", "AND", "WHILE", "WEND", "EOF"] 

def main():
	
	symb = SymbolTable()
	try:
		#inpFile = "inputs.vbs"
		inpFile = sys.argv[1]
	except IndexError:
		print("failed to find file")
		sys.exit(1)

	with open(inpFile, "r") as file:
		inp = file.read() +"\n"
	try:
		inp = inp.replace("\\n", "\n") 
		out = Parser.run(inp)
		out.Evaluate(symb)
	except Exception as err:
		print(err)

if __name__== "__main__":
    main()