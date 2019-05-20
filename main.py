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
		c = "" 

		while (self.position<(len(self.origin)) and (self.origin[self.position]).isspace() and self.origin[self.position] != "\n"): #for white spaces
			self.position += 1
			
		if self.position == len(self.origin):
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
					if (temp == "INTEGER") or (temp == "BOOLEAN"):
						token = Token("TYPE", temp) 
						self.current = token
					else:	 
						token = Token(temp, temp) 
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
		proCode = (PrePro.filter(stg)).lower()
		Parser.token = Tokenizer(proCode) #previously missed something here
		#Parser.token.selectNext()
		tree = Parser.Program()
		return tree

	def parserFactor():
		if Parser.token.current.ttype == INT:
			total = IntVal(Parser.token.current.tvalue, [])
			Parser.token.selectNext()

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

		elif Parser.token.current.ttype == "NOT":
			Parser.token.selectNext()
			children = [Parser.parserFactor()]
			total = UnOp("not",children)

		elif Parser.token.current.ttype == "TRUE":
			total = BoolValue(True)
			Parser.token.selectNext()

		elif Parser.token.current.ttype == "FALSE":
			total = BoolValue(False)
			Parser.token.selectNext()

		elif Parser.token.current.ttype == INPT:
			total = InputOp([],[])
			Parser.token.selectNext()

		elif Parser.token.current.ttype == POPN:
			Parser.token.selectNext()
			total = Parser.parserRelExpression()
			if Parser.token.current.ttype == PCLS:
				Parser.token.selectNext()
			else:
				raise Exception("Error - missing parenthesis )")

		else:
			raise Exception("Error - unidentified token - " + str(Parser.token.current.tvalue))

		return total

	def parserTerm():
		total = Parser.parserFactor()
		mdalist = ["MULT","DIV","AND"]
		while Parser.token.current.ttype in mdalist:
			if Parser.token.current.ttype == MULT: 
				Parser.token.selectNext()
				children = [total, Parser.parserFactor()]
				total = BinOp("*", children)

			if Parser.token.current.ttype == DIV:
				Parser.token.selectNext()
				children = [total, Parser.parserFactor()]
				total = BinOp("/", children)

			if Parser.token.current.ttype == "AND":
				Parser.token.selectNext()
				children = [total, Parser.parserFactor()]
				total = BinOp("and", children)
		
		return total

	@staticmethod
	def parserExpression():
		total = Parser.parserTerm() #priority 
		oplist = ["PLUS", "MINUS", "OR"]
		while Parser.token.current.ttype in oplist: 
			if Parser.token.current.ttype == PLUS: 
				Parser.token.selectNext()
				children = [total, Parser.parserTerm()]
				total = BinOp("+", children)

			if Parser.token.current.ttype == MINUS:
				Parser.token.selectNext()
				children = [total, Parser.parserTerm()] 
				total = BinOp("-", children)

			if Parser.token.current.ttype == "OR":
				Parser.token.selectNext()
				children = [total, Parser.parserTerm()] 
				total = BinOp("or", children)

		return total

	def parserRelExpression():
		total = Parser.parserExpression() #priority 

		if Parser.token.current.ttype == "=":
			Parser.token.selectNext()
			children = [total, Parser.parserExpression()]
			total = BinOp("=", children)

		if Parser.token.current.ttype == GRTT: #greater than
			Parser.token.selectNext()
			children = [total, Parser.parserExpression()]
			total = BinOp(">", children)

		if Parser.token.current.ttype == LSST: #less than
			Parser.token.selectNext()
			children = [total, Parser.parserExpression()]
			total = BinOp("<", children)

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
				total = Assignment(assign, [Identifier(ident,[]), Parser.parserExpression()])

		elif Parser.token.current.ttype == "DIM":
			Parser.token.selectNext()
			if Parser.token.current.ttype == "IDENTIFIER":
				var = Identifier(Parser.token.current.tvalue,[])
				Parser.token.selectNext()
				if Parser.token.current.ttype == "AS":
					Parser.token.selectNext()
					if Parser.token.current.ttype == "TYPE":
						vartype = Parser.token.current.tvalue
						total = VarDec([var,NodeType(vartype)])
						Parser.token.selectNext()
		
		elif Parser.token.current.ttype == "PRINT":
			Parser.token.selectNext()
			total = Print("PRINT", [Parser.parserExpression()])
		
		elif Parser.token.current.ttype == "WHILE":
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

	def Program():
		tempList = []

		#treating beginning and end of input file
		for i in ["sub", "main", "(", ")", "\n"]:
			if Parser.token.current.tvalue.lower() != i:
				print(i)
				print(Parser.token.current.tvalue.lower())
				raise Exception("Error - check your input file - got "+ Parser.token.current.tvalue)
			Parser.token.selectNext()

		tempList.append(Parser.parserStatement())

		while Parser.token.current.ttype == "\n":
			Parser.token.selectNext()
			tempList.append(Parser.parserStatement())

		if Parser.token.current.tvalue.lower() == "end":
			Parser.token.selectNext()
			if Parser.token.current.tvalue.lower() == "sub":
				return Statements("statements", tempList)


class PrePro:
	def filter(inp_stg):
		#print("Input = " + inp_stg)
		return re.sub("'.*\n","", inp_stg) #replace substrings module

class Assembler():
	ASM_Cmds = []

	def Write(stg):
		Assembler.ASM_Cmds.append(stg)

	def WriteAssembly():
		
		with open ("output.asm", "w+") as outfile:
			for h in AssemblerHeader.split("\n"):
				outfile.write(h+"\n")
			
			for j in Assembler.ASM_Cmds:
				outfile.write(j+"\n")
			
			for f in AssemblerFooter.split("\n"):
				outfile.write(f+"\n")

class Node:

	i = 0
	def __init__(self):
		self.value = None
		self.children = []
		self.id = Node.newId()

	def newId():
		Node.i += 1
		return Node.i

	def Evaluate(self):
		pass

class BinOp(Node): #binary ops -> a(binop)b = c
	def __init__(self, value, children):
		self.value = value
		self.children = children
		self.id = Node.newId()

		if len(children) != 2:
			raise Exception("Error - two children expected, got" +self.children)			

	def Evaluate(self,symb):
		#checking if variables types match so we can go on and do ops!
		var1 = self.children[0].Evaluate(symb)
		Assembler.Write("PUSH EBX")
		var2 = self.children[1].Evaluate(symb)

		if self.value == "+":
			#return (var1 + var2, "integer")
			Assembler.Write("POP EAX")
			Assembler.Write("ADD EAX, EBX")
			Assembler.Write("MOV EBX, EAX")
		elif self.value == "-":
			#return (var1 - var2, "integer")
			Assembler.Write("POP EAX")
			Assembler.Write("SUB EAX, EBX")
			Assembler.Write("MOV EBX, EAX")
		elif self.value == "*":
			#return (var1 * var2, "integer")
			Assembler.Write("POP EAX")
			Assembler.Write("IMUL EBX")
			Assembler.Write("MOV EBX, EAX")
		elif self.value == "/":
			#return (var1 // var2, "integer")
			Assembler.Write("POP EAX")
			Assembler.Write("IDIV EBX")
			Assembler.Write("MOV EBX, EAX")
		elif self.value == "=":
			#return (var1 == var2, "boolean")
			Assembler.Write("POP EAX")
			Assembler.Write("CMP EAX, EBX")
			Assembler.Write("CALL binop_je")
		elif self.value == "<":
			#return (var1 < var2, "boolean")
			Assembler.Write("POP EAX")
			Assembler.Write("CMP EAX, EBX")
			Assembler.Write("CALL binop_jl")
		elif self.value == ">":
			#return (var1 > var2, "boolean")
			Assembler.Write("POP EAX")
			Assembler.Write("CMP EAX, EBX")
			Assembler.Write("CALL binop_jg")
		elif self.value == "or":
			#return (var1 or var2, "boolean")
			Assembler.Write("POP EAX")
			Assembler.Write("OR EAX, EBX")
			Assembler.Write("MOV EBX, EAX")
		elif self.value == "and":
			#return (var1 and var2, "boolean")
			Assembler.Write("POP EAX")
			Assembler.Write("AND EAX, EBX")
			Assembler.Write("MOV EBX, EAX")

class UnOp(Node): #unary ops -> -(a) = -a | -(-a) = a
	def __init__(self, value, children):
		self.value = value
		self.children = children
		self.id = Node.newId()
	
	def Evaluate(self, symb):
		if self.value == "+":
			#return self.children[0].Evaluate(symb)
			Assembler.Write("MOV EAX, 1")
			Assembler.Write("IMUL EBX")
			Assembler.Write("MOV EBX, EAX")
		elif self.value == "-":
			#var = self.children[0].Evaluate(symb)
			#var = (var[0]*-1,var[1])
			#return var
			Assembler.Write("MOV EAX, -1")
			Assembler.Write("IMUL EBX")
			Assembler.Write("MOV EBX, EAX")
		elif self.value == "not":
			#var = self.children[0].Evaluate(symb)
			#var = (not var[0],var[1])		
			#return var
			Assembler.Write("NEG EBX")
		else:
			raise Exception("Error - undefined UnOp: "+ str(self.value))

class IntVal(Node): #gets and returns int
	def __init__(self, value, children): 
		self.value = value
		self.children = children	
		self.id = Node.newId()
	
	def Evaluate(self, symb):
		#return (self.value,"integer")
		Assembler.Write("MOV EBX, "+str(self.value))

class NoOp(Node): #dummy - nothing to do here
	def __init__(self, value, children):
		self.value = value
		self.children = children	
		self.id =  Node.newId()

	def Evaluate(self,symb):
		pass

class Assignment(Node): #sets value to given variable - a = K
	def __init__(self, value, children):
		self.value = value
		self.children = children
		self.id = Node.newId()
	
	def Evaluate(self, symb):
		symb.setter(self.children[0].value, self.children[1].Evaluate(symb))

		Assembler.Write("MOV [EBP-"+str(symb.getter(self.children[0].value)[2])+"], EBX")


class Identifier(Node):
	def __init__(self, value, children):
		self.value = value
		self.children = children
		self.id = Node.newId()
	
	def Evaluate(self, symb):
		#return symb.getter(self.value)
		Assembler.Write("MOV EBX, [EBP-"+str(symb.getter(self.value)[2])+"]")

class Statements(Node): #statement in statements
	def __init__(self, value, children):
		self.value = value
		self.children = children
		self.id = Node.newId()
	
	def Evaluate(self, symb):
		for i in self.children:
			i.Evaluate(symb)

class Print(Node): 
	def __init__(self, value, children):
		self.value = value
		self.children = children
		self.id = Node.newId()
	
	def Evaluate(self,symb):
		self.children[0].Evaluate(symb)
		Assembler.Write("PUSH EBX")
		Assembler.Write("CALL print")
		Assembler.Write("POP EBX")

class WhileOp(Node):
	def __init__(self, value, children):
		self.value = value
		self.children = children
		self.id = Node.newId()

	def Evaluate(self,symb):
		Assembler.Write("LOOP_"+str(self.id)+":")

		self.children[0].Evaluate(symb)

		Assembler.Write("CMP EBX, False")
		Assembler.Write("JE EXIT_"+str(self.id))

		self.children[1].Evaluate(symb)

		Assembler.Write("JMP LOOP_"+str(self.id))
		Assembler.Write("EXIT_"+str(self.id)+":")

class IfOp(Node):
	def __init__(self, children):
		self.children = children
		self.id = Node.newId()
	
	def Evaluate(self,symb):

		Assembler.Write("CMP EBX, True")
		Assembler.Write("JE if_"+str(self.id))

		if self.children[0].Evaluate(symb)[1] == 'boolean':
			self.children[1].Evaluate(symb)
		else:
			if len(self.children) == 3:
				self.children[2].Evaluate(symb)
			else:
				pass

		Assembler.Write("JMP EXIT_"+str(self.id))
		Assembler.Write("if_"+str(self.id))
		Assembler.Write("EXIT_"+str(self.id))

class InputOp(Node):
	def __init__(self, value,children):
		self.value = value
		self.children = children
		self.id = Node.newId()
	
	def Evaluate(self,symb):
		#return (int(input()),"integer")
		pass

class NodeType(Node):
	def __init__(self, value):
		self.value = value
		self.id = Node.newId()
		#temptrylist = ["integer","boolean"]
		#if value.lower() not in temptrylist:
		#	raise Exception("Error - unexpected type " + str(self.value))
			
	def Evaluate(self, symb):
		#if self.value == "integer":
		#	return (self.value,0)
		#elif self.value == "boolean":
		#	return (self.value, False)
		pass

class SymbolTable:
	def __init__(self):
		self.varDict = {}
		self.shift = 0

	def getter(self, var): #returns value for variable
		if var in self.varDict.keys():
			return self.varDict[var]
		else:
			raise Exception("Error - undeclared variable")

	def setter(self, var, value): #assigns value to variable
		if var not in self.varDict:
			raise Exception("Error - undeclared variable")		
		self.varDict[var][0] = value
	
	def declarator(self, var, value, tp):
		if var in self.varDict:
			raise Exception("Error - duplicate variable")
		self.shift += 4
		self.varDict[var] = [None, tp, self.shift]

class VarDec(Node):
	def __init__(self, children):
		self.children = children
		self.id = Node.newId()
	
	def Evaluate(self, symb):
		symb.declarator(self.children[0].value, None, self.children[1].Evaluate(symb))
		Assembler.Write("PUSH DWORD 0")

class BoolValue(Node):
	def __init__(self, value):
		self.value = value
		self.id = Node.newId()
	
	def Evaluate(self,symb):
		#return (self.value,"boolean")
		Assembler.Write("MOV EBX, "+str(self.value))


#Tokens -- THIS IS A MESS AND I REGRET DOING THIS FOR REAL
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
RWL = ["BEGIN", "END", "PRINT", "IF", "THEN", "ELSE", "OR", "AND", "WHILE", "WEND", "EOF",
		"INPUT", "NOT", "DIM", "INTEGER", "BOOLEAN", "TRUE", "FALSE", "AS", "MAIN", "SUB"] 

AssemblerHeader = """; constantes
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0

segment . data

segment . bss ; variaveis
  res RESB 1

section .text
  global_start

print:  ; subrotina print
  PUSH EBP ; guarda o base pointer
  MOV EBP, ESP ; estabelece um novo base pointer

  MOV EAX, [EBP+8] ; 1 argumento antes do RET e EBP
  XOR ESI, ESI

print_dec: ; empilha todos os digitos
  MOV EDX, 0
  MOV EBX, 0x000A
  DIV EBX
  ADD EDX, '0'
  PUSH EDX
  INC ESI ; contador de digitos
  CMP EAX, 0
  JZ print_next ; quando acabar pula
  JMP print_dec

print_next:
  CMP ESI, 0
  JZ print_exit ; quando acabar de imprimir
  DEC ESI

  MOV EAX, SYS_WRITE
  MOV EBX, STDOUT

  POP ECX
  MOV [res], ECX
  MOV ECX, res

  MOV EDX, 1
  INT 0x80
  JMP print_next

print_exit:
  POP EBP
  RET

; subrotinas if/while
binop_je:
  JE binop_true
  JMP binop_false

binop_jg:
  JG binop_true
  JMP binop_false

binop_jl:
  JL binop_true
  JMP binop_false

binop_false:
  MOV EBX, False  
  JMP binop_exit
binop_true:
  MOV EBX, True
binop_exit:
  RET
"""

AssemblerFooter = """
; interrupcao de saida
POP EBP
MOV EAX, 1
INT 0 x80
"""


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
		Assembler.WriteAssembly()
	except Exception as err:
		print(err)

if __name__== "__main__":
    main()