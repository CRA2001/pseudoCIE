'''
this is the parser for pseudoCIE, it basically takes the return value
from lexer.py's tokenize() method (from the lexer class), and applies
recursive descent on to it to construct the AST STRUCTURE
'''

from lexer import Lexer #importing from lexer.py to take in the array of tokens

class Parser:
	#constructor for parser which takes in the tokens and the current position
	def __init__(self,tokens):
		self.tokens = tokens
		self.pos = 0
	def current_token(self):
		#tracking the token
		#if the position is still inside of range of amount of elements in the token array
		# then return the token at the current position
		return self.tokens[self.pos] if self.pos < len(self.tokens) else None

	def consume(self,token_type):
		#determining whether or not the current token and the token type at the current tuple match with
		#parameter token type 
		if self.current_token() and self.current_token()[0] == token_type:
			self.pos+=1
		else:
		#if it isn't then raise a syntax error
			raise SyntaxError(f"Expected token type: {token_type}, got {self.current_token()} instead")
		
	def parse_expr(self):
		left = self.current_token()[1]
		if self.current_token()[0] == 'NUMBER':
			self.consume('NUMBER')
		elif self.current_token()[0] == 'IDENTIFIER':
			self.consume("IDENTIFIER")
		while self.current_token() and self.current_token()[0] in ('PLUS','MINUS','MULTIPLY','DIVIDE'):
			op = self.current_token()[0]
			self.consume(op)
			right = self.tokens[self.pos][1]
			self.consume('NUMBER')
			if op =='PLUS':
				left = ('ADD',left,right)
			elif op =='MINUS':
				left = ('SUB',left,right)
			elif op == 'MULTIPLY':
				left = ('MULTIPLY',left,right)
			elif op == 'DIVIDE':
				left = ('DIVIDE',left,right)
		return left
	
	def parse(self):
		statements = []
		while self.current_token():
			if self.current_token()[0] == "IDENTIFIER" and self.tokens[self.pos+1][0] == 'ASSIGN':
				var_name = self.current_token()[1]
				self.consume('IDENTIFIER')
				self.consume('ASSIGN')
				expr = self.parse_expr() #parse from the right hand side
				statements.append(('ASSIGN',var_name,expr))
			
			else:
				statements.append(self.parse_expr())
		return statements



		# self.consume('PLUS')
		# right = self.current_token()[1]
		# self.consume('NUMBER')
		# return ('ADD',left,right)
	

if __name__ == "__main__":
	print("Test 1: Multiline code:")
	pseudocode = '''
	x <- 2 + 1
	y <- 3 + 4
	'''
	l = Lexer(pseudocode)
	tokens = l.tokenize()
	print("Tokens")
	print(tokens)
	p = Parser(tokens)
	ast = p.parse()
	print("AST: ", ast)