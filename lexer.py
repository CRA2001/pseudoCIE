import re

class Lexer:
    def __init__(self,code):
        self.code = code # this will hold the code to run
        self.tokens = [] #will store all the tokens found inside the code
        self.pos = 0 #used to track the scanning process in lexical analysis
        #token patterns that will be compared with the code given, where each pattern will be a tuple (<type category of tuple>, <regEx_pattern>) 
        self.t_spec = [
            #Control statements - CONDITIONALS
            ('IF',r'\bIF\b'),
            ('THEN',r'\bTHEN\b'),
            ('ELSE',r'\bELSE\b'),
            ('ENDIF',r'\bENDIF\b'),
            ('AND',r'\bAND\b'),
            ('OR',r'\bOR\b'),
            #Operators
            ('ASSIGN',r'<-'),
            ('EQ',r'='),
            ('GT',r'>'),
            ('LT',r'<'),
            ('GTE',r'>='),
            ('LTE',r'<='),
            ('PLUS',r'\+'),
            ('MINUS',r'\-'),
            ('MULTIPLY',r'\*'),
            ('DIVIDE',r'/'),
            ('LPAREN',r'\('),
            ('RPAREN',r'\)'),
            #Data types
            ('NUMBER',r'\b\d+\b'), #integer values
            ('IDENTIFIER',r'\b[A-Za-z_]\w*\b'),
            #Ignore this shit
            ('SKIP',r'[ \t]+'),
            #Catch unexpected characters
            ('MISMATCH',r'.')
        ]

        #compiling the paterns
        self.token_regex = re.compile('|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in self.t_spec ))

    def tokenize(self):
        #tokenization process (input code into tokens)
        for match in self.token_regex.finditer(self.code):
            token_type= match.lastgroup
            token_value = match.group(token_type)
            if token_type == "NUMBER":
                token_value = int(token_value) #converting it into a number 
            elif token_type == 'SKIP' or token_type == 'NEWLINE':
                continue #ignore the non-tokens
            elif token_type == 'MISMATCH':
                raise RuntimeError(f'Unexpected character: {token_value!r}')

            self.tokens.append((token_type,token_value))
        return self.tokens



# test code

if __name__ == '__main__':
    print('test1: simple expressions')
    pseudocode = """
    x <- 5+3 
    y <- x * 2

    """
    lexer = Lexer(pseudocode)
    tokens = lexer.tokenize()

    print("Tokens:")
    print(tokens)

    print('test2: relational operators')
    pseudocode = '''
    x <- 5 AND y <-3 OR z <-10
    '''
    lexer_instance = Lexer(pseudocode)
    tokens=lexer.tokenize()
    print(tokens)

    print('test3: conditionals')
    pseudocode = '''
    x <- 5 
    IF x > 5 THEN
        y <- x*2
    ELSE
        y <- x - 2
    '''
    lexer = Lexer(pseudocode)
    tokens = lexer.tokenize()
    print(tokens)


    
