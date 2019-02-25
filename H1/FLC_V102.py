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
		c = 0 #input placeholder

		if self.position >= len(self.origin): #this means we got to the end of the input and we'll have to add something there
			token = Token(END,'void')
			self.current=token

		#going back to V0.1.X
		elif self.origin[self.position].isdigit():
			while (self.position<(len(self.origin)) and (self.origin[self.position]).isdigit()): #we'll be good till we find a symbol/reach the end of inp
				c += int(self.origin[self.position]) #stores the number
				#print(self.position)
				self.position += 1
			#print("hello there "+str(self.position))
			token = Token(DIG, c)
			self.current = token

		elif self.origin[self.position] == "+": #we're about to sum something!
			token = Token(SUM, "+") 
			self.position += 1
			self.current = token
			
		elif self.origin[self.position] == "-": #we're about to subtract something!
			token = Token(SUB, "-") 
			self.position += 1
			self.current = token

class Parser: #token parser
	token = None
	def start(stg):
		total = 0
		Parser.token = Tokenizador(stg) #let the fun begin	
		Parser.token.selectNext()
		#print(Parser.token.current.ttype)
		#print(Parser.token.current.tvalue)

		if Parser.token.current.ttype == DIG:
			total += Parser.token.current.tvalue
			Parser.token.selectNext()
			while Parser.token.current.ttype != END: #breaks after end of input string

				if Parser.token.current.ttype == SUM: 
					Parser.token.selectNext()
					if Parser.token.current.ttype == DIG:
						total += Parser.token.current.tvalue

				elif Parser.token.current.ttype == SUB:
					Parser.token.selectNext()
					if Parser.token.current.ttype == DIG:
						total -= Parser.token.current.tvalue

				else:
					print("Error - Should have been an op")
					break

				Parser.token.selectNext()
		else:
			print("Error - Should have been a digit")

		print("Result = "+str(total)+"\n")
		return total

#Tokens
SUM = "SUM" #sum
SUB = "SUB" #subtract
DIG = "DIG" #digit
END = "I-END" #end of input

def main():
	#now we have to make a "CLASSy" input... got it?
	x = input("Por obséquio, insira uma operação matemática a qual vossa senhoria detenha aspiração em realizar ")
	x = x.replace(" ", "")
	print("")
	print("Input = "+x)
	Parser.start(x)

if __name__== "__main__":
    main()









