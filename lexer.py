import re

class Lexer:
    def __init__(self,code):
        self.code = code # this will hold the code to run
        self.tokens = [] #will store all the tokens found inside the code
        self.pos = 0 #used to track the scanning process in lexical analysis
        #token patterns that will be compared with the code given, where each pattern will be a tuple (<type category of tuple>, <regEx_pattern>) 
        self.t_spec = [
            ('OUTPUT',r'\bOUTPUT\b'),
            ("COMMENT",r'//.*'), #comments
            ("REAL",r'\d+\.\d+'),
            ("STRING",r'"[^"]*"'),
            ("BOOLEAN",r'\bTRUE\b|\bFALSE\b'),
            ("IDENTIFIER",r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
            ('ASSIGN','<-'),            
            ('NUMBER',r'\b\d+\b'),
            ('PLUS',r'\+'),
            ('MINUS',r'\-'),
            ('MULTIPLY',r'\*'),
            ('DIVIDE',r'/'),
            ('SKIP',r'[ \t]+'),
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
            elif token_type == 'REAL':
                token_value = float(token_value)
            elif token_type == "BOOLEAN":
                token_value = True if token_value == "TRUE" else False
            elif token_type == "STRING":
                token_value = token_value.strip('"')
            elif token_type == 'COMMENT':
                continue #ignores comments which is considered a non-token
            elif token_type == 'SKIP' or token_type == 'NEWLINE':
                continue #ignore the non-tokens
            elif token_type == 'MISMATCH':
                raise RuntimeError(f'Unexpected character: {token_value!r}')
            
            self.tokens.append((token_type,token_value))
        return self.tokens



# test code

if __name__ == '__main__':
    # print('test1: simple expressions')
    # pseudocode = "2+3"
    # lexer = Lexer(pseudocode)
    # tokens = lexer.tokenize()

    # print("Tokens:")
    # print(tokens)
    
    print("Test 2: variable and assignments")
    pseudocode = '''
    x <- 3    
    '''
    lexer=Lexer(pseudocode)
    tokens=lexer.tokenize()
    print(f"Tokens {tokens}")
    print("Test 3: variable and assignments with arithmetic")
    pseudocode = '''
    x <- 3 + 4    
    '''
    lexer=Lexer(pseudocode)
    tokens=lexer.tokenize()
    print(f"Tokens {tokens}")