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
		if self.current_token()[0] == 'NUMBER':
			left = self.current_token()[1]
			self.consume('NUMBER')
		elif self.current_token()[0] == 'IDENTIFIER':
			left = self.current_token()[1]
			self.consume("IDENTIFIER")
		elif self.current_token()[0] == 'STRING':
			left = ('STRING',self.current_token()[1])
			self.consume('STRING')
		else:
			raise SyntaxError(f"Unexpected token: {self.current_token()}")

		# handling expressions with + - * /
		while self.current_token() and self.current_token()[0] in ('PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE'):
			op = self.current_token()[0]
			self.consume(op)

			if self.current_token()[0] == 'NUMBER':
				right = self.current_token()[1]
				self.consume('NUMBER')
			elif self.current_token()[0] == 'IDENTIFIER':
				right = self.current_token()[1]
				self.consume("IDENTIFIER")
			elif self.current_token()[0] == 'STRING':
				right = ('STRING', self.current_token()[1])
				self.consume('STRING')
			else:
				raise SyntaxError(f"Expected NUMBER, IDENTIFIER, or STRING, got {self.current_token()}")
			if op == 'PLUS':
				left = ('ADD', left, right)
			elif op == 'MINUS':
				left = ('SUB', left, right)
			elif op == 'MULTIPLY':
				left = ('MULTIPLY', left, right)
			elif op == 'DIVIDE':
				left = ('DIVIDE', left, right)
		while self.current_token() and self.current_token()[0] in ('GREATER_THAN','LESS_THAN','EQUAL_TO','NOT_EQUAL_TO', 'GREATER_THAN_OR_EQUAL','LESS_THAN_OR_EQUAL'):
			op = self.current_token()[0]
			self.consume(op)
			right = self.parse_expr()
			left = (op,left,right)

		return left

	def parse_block_until(self,stop_token):
		block = []
		while self.current_token() and self.current_token()[0] not in stop_token:
			block.append(self.parse_statement())
		return block
	
	def parse_while(self):
		self.consume('WHILE')
		condition = self.parse_expr()
		self.consume('DO')
		body = self.parse_block_until(['END_WHILE'])
		self.consume('END_WHILE')
		return ('WHILE',condition,body)
	
	def parse_for(self):
		self.consume("FOR")
		var_name = self.current_token()[1]
		self.consume('IDENTIFIER')
		self.consume('ASSIGN')
		start = self.parse_expr()
		self.consume('TO')
		end = self.parse_expr()

		body = self.parse_block_until(['NEXT'])
		self.consume('NEXT')
		next_var = self.current_token()[1]
		self.consume('IDENTIFIER')

		if next_var != var_name:
			raise SyntaxError(f"NEXT variable '{next_var}' doesn't match FOR variable ")
		return ('FOR',var_name,start,end,body)
	

	def parse_if(self):
		self.consume("IF")
		condition = self.parse_expr()
		self.consume("THEN")

		then_branch = self.parse_block_until(['ELSE','ENDIF'])
		token = self.current_token()
		if self.current_token() and self.current_token()[0] == 'ELSE':
			self.consume("ELSE")
			else_branch = self.parse_block_until(['ENDIF'])
			self.consume('ENDIF')
		else:
			else_branch = None
			self.consume('ENDIF')

		return ('IF',condition,then_branch,else_branch)
	
	def parse_statement(self):
		if self.current_token()[0] == "IDENTIFIER" and self.tokens[self.pos+1][0] == 'ASSIGN':
			var_name = self.current_token()[1]
			self.consume('IDENTIFIER')
			self.consume('ASSIGN')
			expr = self.parse_expr() #parse from the right hand side
			return ('ASSIGN',var_name,expr)
		elif self.current_token()[0] == "OUTPUT":
			self.consume('OUTPUT')
			expr = self.parse_expr()
			return ("OUTPUT",expr)
		elif self.current_token()[0] == "IF":
			return self.parse_if()
		elif self.current_token()[0] == "FOR":
			return self.parse_for()
		elif self.current_token()[0] == "WHILE":
			return self.parse_while()
		else:
			return self.parse_expr()
		

	def parse(self):
		statements = []
		while self.current_token():
			statements.append(self.parse_statement())
		return statements

if __name__ == "__main__":
	test_code_1 = '''
	WHILE a < 10 DO
		OUTPUT a
		a <- a + 1
	END WHILE
	'''
	l = Lexer(test_code_1)
	t = l.tokenize()
	print("Tokens: \n ", t)
	p = Parser(t)
	print("AST: ",p.parse())