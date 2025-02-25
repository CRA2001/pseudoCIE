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
		if self.pos < len(self.tokens):
			return self.tokens[self.pos]
		return None


	def moveToNext(self,token_type):
		if self.current_token() and self.current_token()[0] == token_type:
			self.pos+=1
		else:
			raise SyntaxError(f"Expected token type: {token_type}, got {self.current_token()} instead")
	def parse(self):
		#calling the expression() recursive function to control the call()
		return self.expression()
	def expression(self):
		node = self.term()
		while self.current_token() and self.current_token()[0] in ('PLUS','MINUS'):
			token = self.current_token()
			self.moveToNext(token[0])
			node = ('binary_op',token[0],node,self.term())
		return node
	def term(self):
		node = self.factor()
		while self.current_token() and self.current_token()[0] in ('MULTIPLY','DIVIDE'):
			token = self.current_token()
			self.moveToNext(token[0])
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
	code =  "3+5 * (2-1)"
	lexer_instance = lexer.Lexer(code)
	tokens = lexer_instance.tokenize()
	print("Tokens",tokens)
	parser = Parser(tokens)
	ast = parser.parse()
	print("Parsed AST: ",ast)





