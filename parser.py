'''
this is the parser for pseudoCIE, it basically takes the return value
from lexer.py's tokenize() method (from the lexer class), and applies
recursive descent on to it to construct the AST STRUCTURE
'''

import lexer #importing from lexer.py to take in the array of tokens

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
		'''
		if self.pos < len(self.tokens):
			return self.tokens[self.pos]
		return None
		'''

	def moveToNext(self,token_type):
		#determining whether or not the current token and the token type at the current tuple match with
		#parameter token type 
		if self.current_token() and self.current_token()[0] == token_type:
			self.pos+=1
		else:
		#if it isn't then raise a syntax error
			raise SyntaxError(f"Expected token type: {token_type}, got {self.current_token()} instead")
	def parse(self):
		#calling the expression() recursive function to control the call()
		return self.expression()
	def expression(self):
		#forming the node to store the token
		node = self.term()
		#while the token is a minus or a plus operator
		while self.current_token() and self.current_token()[0] in ('PLUS','MINUS'):
			#instantiate the current token as the attribute self.current_token()
			token = self.current_token()
			# call the self.moveToNext() function to confirm whether to move forward or not
			self.moveToNext(token[0])
			#adding it to the AST
			node = ('binary_op',token[0],node,self.term())
		return node
	def term(self):
		#forming the node to call the token based from the return of factor()
		node = self.factor()
		#while the token is a multiply or divide operator
		while self.current_token() and self.current_token()[0] in ('MULTIPLY','DIVIDE'):
			#instatiate the current token as the attribute self.current_token
			token = self.current_token()
			#call the self.moveToNext() function to confirm whether to move forward or not
			self.moveToNext(token[0])
			#adding it to the AST 
			node = ('binary_op',token[0],node,self.term())
		return node

	def factor(self):
		token = self.current_token()
		if token[0] == 'NUMBER':  # Check if it's a number
			self.moveToNext('NUMBER')  # Consume the number token
			return ('number', token[1])  # Return the node representing the number
		elif token[0] == 'LPAREN':  # If it's a left parenthesis
			print("LPAREN FOUND")
			self.moveToNext('LPAREN')  # Consume the LPAREN token
			node = self.expression()  # Parse the expression inside the parentheses
			self.moveToNext('RPAREN')  # Consume the closing RPAREN
			return ('paren', node)  # Return the node wrapped inside 'paren'
		else:
			raise SyntaxError(f'Unexpected token: {token}')


#test value
if __name__ == "__main__":
	print("TEST Number 1")
	code =  "3+5 * (2-1)"
	lexer_instance = lexer.Lexer(code)
	tokens = lexer_instance.tokenize()
	print("Tokens",tokens)
	parser = Parser(tokens)
	ast = parser.parse()
	print("Parsed AST: ",ast)
