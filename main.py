import re #regular expressions

class Token:
	def __init__(self, ttype, tvalue):
		self.ttype = ttype
		self.tvalue = tvalue

class Tokenizer:
	def __init__(self, origin):
		self.origin = origin
		self.position = 0
		self.current = Token(END, END)

	def selectNext(self): #updates position
		c = "" #input placeholder | previously a number, troublemaker that made me sad and literally caused V1.0.3

		if self.position >= len(self.origin): #this means we got to the end of the input and we'll have to add something there
			token = Token(END,"I-END")
			self.current=token

		#going back to V0.1.X
		elif self.origin[self.position].isdigit():
			while (self.position<(len(self.origin)) and (self.origin[self.position]).isdigit()): #we'll be good till we find a symbol/reach the end of inp
				c += self.origin[self.position] #stores the number
				#print(self.position)
				self.position += 1
			#print("hello there "+str(self.position))
			c = int(c)
			token = Token(INT, c)
			self.current = token

		elif self.origin[self.position] == "+": #we're about to sum something!
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
			token = Token("(", "(")
			self.position += 1
			self.current = token
		
		elif self.origin[self.position] == ')': #we're about to end someone's priority!
			token = Token(")", ")")
			self.position += 1
			self.current = token
		
		else:
			raise Exception("Token not found")

class Parser: #token parser
	token = None

	@staticmethod 
	def start(stg):
		total = 0 
		Parser.token = Tokenizer(stg) #let the fun begin	
		Parser.token.selectNext()

	def parserFactor():
		total = 0
		if Parser.token.current.ttype == INT:
			total = Parser.token.current.tvalue
			Parser.token.selectNext()
		
		elif Parser.token.current.ttype == "(":
			Parser.token.selectNext()
			total = Parser.parserExpression()
			if Parser.token.current.ttype == ")":
				Parser.token.selectNext()
			else:
				raise Exception("Error - missing parenthesis )")

		elif Parser.token.current.ttype == PLUS: 
			Parser.token.selectNext()
			total += Parser.parserFactor()

		elif Parser.token.current.ttype == MINUS:
			Parser.token.selectNext()
			total -=  Parser.parserFactor()

		return total

	def parserTerm():
		total = Parser.parserFactor()
		while Parser.token.current.ttype == MULT or Parser.token.current.ttype == DIV:
			if Parser.token.current.ttype == MULT: 
				Parser.token.selectNext()
				total *= Parser.parserFactor()

			if Parser.token.current.ttype == DIV:
				Parser.token.selectNext()
				total //= Parser.parserFactor()
			"""
				else:
					raise Exception("Error - Should have been a digit - DIV")
			else:
				raise Exception("Error - Should have been an operator - MULT/DIV")
			"""
		
		return total


	@staticmethod
	def parserExpression():
		total = Parser.parserTerm() #priority 
		while Parser.token.current.ttype == PLUS or Parser.token.current.ttype == MINUS: 
			if Parser.token.current.ttype == PLUS: 
				Parser.token.selectNext()
				total += Parser.parserTerm()

			if Parser.token.current.ttype == MINUS:
				Parser.token.selectNext()
				total -=  Parser.parserTerm()

		return total

class PrePro:
	@staticmethod
	def filter(inp_stg):
		if("'" not in inp_stg):
			return inp_stg[:-1]
		return re.sub("'.*?\n","", inp_stg) #replace substrings module

#Tokens
PLUS = "PLUS" #sum 
MINUS = "MINUS" #subtract | negative numbers
INT = "INT" #digits (currently ints only)
END = "I-END" #end of input
MULT = "MULT" #multiply
DIV = "DIV" #divide	
POPN = "(" #parenthesis open
PCLS = ")"	#parenthesis close

def main():
	try:
		#done with the CLASSY joke >:(
		x = input("Insira uma expressão ") + "\n"
		x = x.replace("\\n", "\n") #previously this removed spaces and that's not good 
		print("Input = "+x)
		x = PrePro.filter(x)
		Parser.start(x)
		print("Result = "+str(Parser.parserExpression()))
	except Exception as err:
		print(err)


if __name__== "__main__":
    main()