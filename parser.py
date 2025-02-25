'''
this is the parser for pseudoCIE, it basically takes the return value
from lexer.py's tokenize() method (from the lexer class), and applies
recursive descent on to it to construct the AST STRUCTURE
'''

import lexer

class Parser:
	#constructor for parser which takes in the tokens and the current position
	def __init__(self,tokens):
		self.tokens = tokens
		self.pos = 0	
	def current_token(self):
		if self.pos < len(self.tokens):
			return self.tokens[self.pos]
		return None


	def eat(self,token_type):

		if self.current_token() and self.current_token().type() == token_type:
			self.pos+=1
		else:
			raise SyntaxError(f"Expected token type: {token_type}, got {self.current_token()} instead")
	def parse(self):
		#calling the expression() recursive funciton to control the call()
		return self.expression()
	def expression(self):
		node = self.term()
		while self.current_token() and self.current_token().type in ('PLUS','MINUS'):
			token = self.current_token()
			self.eat(token.type)
			node = ('binary_op',token.type,node,self.factor())	
		return node
	def term(self):
		node = self.factor()
		while self.current_token() and self.current_token().type in ('MULTIPLY','DIVIDE'):
			token = self.current_token()
			self.eat(token.type)
			node = ('binary_op',token.type,node,self.factor())	
		return node
	def factor(self):
		token = self.current_token()
		if token.type == 'NUMBER':
			self.eat('NUMBER')
			return ('number',token.value)
		elif token.type == 'LPAREN':
			self.eat('LPAREN')
			node = self.expression()
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












