class Token:
	def __init__(self, ttype, tvalue):
		self.ttype = ttype
		self.tvalue = tvalue

class Tokenizador:
	def __init__(self, origin):
		self.origin = origin
		self.position = 0
		self.current = Token(END, END)
		
	def selectNext(self): #updates position
		c = "" #input placeholder | previously a number, troublemaker that made me sad and literally caused V1.0.3

		if self.position >= len(self.origin): #this means we got to the end of the input and we'll have to add something there
			token = Token(END,"finale")
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

class Parser: #token parser
	token = None

	@staticmethod 
	def start(stg):
		total = 0 
		Parser.token = Tokenizador(stg) #let the fun begin	
		Parser.token.selectNext()

	@staticmethod
	def parseExpression():
		if Parser.token.current.ttype == INT:
			total = Parser.token.current.tvalue
			Parser.token.selectNext()
			while Parser.token.current.ttype != END: #breaks after end of input string

				if Parser.token.current.ttype == PLUS: 
					Parser.token.selectNext()
					if Parser.token.current.ttype == INT:
						total += Parser.token.current.tvalue
					else:
						raise Exception("Error - Should have been a digit")

				elif Parser.token.current.ttype == MINUS:
					Parser.token.selectNext()
					if Parser.token.current.ttype == INT:
						total -= Parser.token.current.tvalue
					else:
						raise Exception("Error - Should have been a digit")
				else:
					raise Exception("Error - Should have been an op")
				Parser.token.selectNext()
		else:
			raise Exception("Error - Should have been a digit")

		print("Result = "+str(total)+"\n")
		return total

#Tokens
PLUS = "PLUS" #sum 
MINUS = "MINUS" #subtract | negative numbers
INT = "INT" #digits (currently ints only)
END = "I-END" #end of input

def main():
	try:
		#now we have to make a "CLASSy" input... got it?
		x = input("Por obséquio, insira uma operação matemática a qual vossa senhoria detenha aspiração em realizar ")
		x = x.replace(" ", "")
		print("")
		print("Input = "+x)
		Parser.start(x)
		Parser.parseExpression()
	except Exception as err:
		print(err)


if __name__== "__main__":
    main()