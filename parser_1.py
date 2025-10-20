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


	#handling the expressions	
	def parse_expr(self):
		if self.current_token()[0] == 'NUMBER':
			left = self.current_token()[1]
			self.consume('NUMBER')
		elif self.current_token()[0] == 'IDENTIFIER':
			var_name = self.current_token()[1]
			self.consume("IDENTIFIER")

			if self.current_token() and self.current_token()[0] == 'LBRACKET':
				self.consume('LBRACKET')
				index_expr = self.parse_expr()
				self.consume('RBRACKET')
				left = ('INDEX',var_name,index_expr)
			else:
				left = var_name
			
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
	
	#handling while loops
	def parse_while(self):
		self.consume('WHILE')
		condition = self.parse_expr()
		self.consume('DO')
		body = self.parse_block_until(['END_WHILE'])
		self.consume('END_WHILE')
		return ('WHILE',condition,body)
	#handling for loops
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
	
	#handling declare keyword
	def parse_declare(self):
		self.consume('DECLARE')
		var_name = self.current_token()[1]
		self.consume('IDENTIFIER')
		self.consume('COLON')

		# --- ARRAY declarations ---
		if self.current_token()[0] == "ARRAY_DTYPE":
			self.consume('ARRAY_DTYPE')

			bounds_list = []

			# Case 1: single-token bound like "[1:5]"
			if self.current_token()[0] == 'BOUND':
				raw_bounds = self.current_token()[1]  # "[1:5]" or "[1:2,1:3]"
				self.consume('BOUND')

				# Handle multi-dimensional inside single token
				raw_bounds = raw_bounds.strip('[]')
				for part in raw_bounds.split(','):
					lo, hi = part.split(':')
					bounds_list.append((int(lo), int(hi)))

			# Case 2: expanded token form [ 1 : 3 , 1 : 4 ]
			elif self.current_token()[0] == 'LBRACKET':
				self.consume('LBRACKET')
				while True:
					if self.current_token()[0] != 'NUMBER':
						raise SyntaxError(f"Expected NUMBER in array bounds, got {self.current_token()}")
					lo = int(self.current_token()[1])
					self.consume('NUMBER')

					self.consume('COLON')

					if self.current_token()[0] != 'NUMBER':
						raise SyntaxError(f"Expected NUMBER in array bounds, got {self.current_token()}")
					hi = int(self.current_token()[1])
					self.consume('NUMBER')

					bounds_list.append((lo, hi))

					if self.current_token() and self.current_token()[0] == 'COMMA':
						self.consume('COMMA')
						continue
					break
				self.consume('RBRACKET')
			else:
				raise SyntaxError(f"Expected array bounds after ARRAY, got {self.current_token()}")

			self.consume('OF')

			if self.current_token()[0] not in ('INTEGER_DTYPE', 'REAL_DTYPE', 'BOOLEAN_DTYPE', 'STRING_DTYPE'):
				raise SyntaxError(f"Expected base type after OF, got {self.current_token()}")

			base_type = self.current_token()[0]
			self.consume(base_type)

			return ('DECLARE', var_name, ('ARRAY', bounds_list, base_type))

		# --- Scalar declarations ---
		elif self.current_token()[0] in ('INTEGER_DTYPE', 'REAL_DTYPE', 'BOOLEAN_DTYPE', 'STRING_DTYPE'):
			data_type = self.current_token()[0]
			self.consume(data_type)
			return ('DECLARE', var_name, data_type)

		else:
			raise SyntaxError(f"Got: {self.current_token()}, expected datatype or ARRAY")

	#handling the if statements
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
	
	#handling input from user 
	def parse_input(self):
		self.consume('INPUT')
		var_name = self.current_token()[1]
		self.consume('IDENTIFIER')
		return ('INPUT',var_name)

	#handling array index access of values	
	def parse_array_access(self):
		name = self.current_token()[1]
		self.consume('IDENTIFIER')
		self.consume('LBRACKET')

		# Support multiple indices: [i], [i,j], [i,j,k], etc.
		indices = [self.parse_expr()]
		while self.current_token() and self.current_token()[0] == 'COMMA':
			self.consume('COMMA')
			indices.append(self.parse_expr())

		self.consume('RBRACKET')
		return ('INDEX', name, indices)

	#handling the calls of methods for each token based on the type of token
	def parse_statement(self):
		if self.current_token()[0] == "IDENTIFIER" and self.tokens[self.pos+1][0] in ("LBRACKET", "ASSIGN"):
			# Peek ahead to check what kind of statement it is
			if self.tokens[self.pos+1][0] == "LBRACKET":
				# Parse array access (supports multiple indices)
				array_access = self.parse_array_access()
				self.consume("ASSIGN")
				value_expr = self.parse_expr()
				# array_access = ('INDEX', name, [index_exprs])
				return ("ARRAY_ASSIGN", array_access[1], array_access[2], value_expr)
			else:
				# Regular variable assignment
				var_name = self.current_token()[1]
				self.consume('IDENTIFIER')
				self.consume('ASSIGN')
				expr = self.parse_expr()
				return ('ASSIGN', var_name, expr)
		
		elif self.current_token()[0] == "DECLARE":
			return self.parse_declare()
		elif self.current_token()[0] == "OUTPUT":
			self.consume('OUTPUT')
			expr = self.parse_expr()
			return ("OUTPUT", expr)
		elif self.current_token()[0] == "INPUT":
			return self.parse_input()
		elif self.current_token()[0] == "IF":
			return self.parse_if()
		elif self.current_token()[0] == "FOR":
			return self.parse_for()
		elif self.current_token()[0] == "WHILE":
			return self.parse_while()
		else:
			return self.parse_expr()

		
	#returns abstract syntax tree
	def parse(self):
		statements = []
		while self.current_token():
			statements.append(self.parse_statement())
		return statements
	
if __name__ == '__main__':
    print("TEST CODE 1: ")
    test_code_1 = '''
    DECLARE Grid : ARRAY[1:2,1:3] OF INTEGER
    '''
    l = Lexer(test_code_1)
    t = l.tokenize()
    p = Parser(t)
    print(p.parse())