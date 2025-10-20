#importing all the other parts of the compiler
from lexer import Lexer
from parser_1 import Parser
from semantic import Evaluator

def run_code(code):
    #step 1: tokenize the code
    lexer = Lexer(code)
    tokens=lexer.tokenize()
    #step 2: parse tokens into AST
    parser = Parser(tokens)
    ast = parser.parse()
    #step 3: evaluate the AST to get resule
    evaluator = Evaluator()
    result = evaluator.evaluate(ast)
    return result

if __name__ == '__main__':
    with open("ExternalTest.txt",'r') as f:
        code = f.read()
        run_code(code)
 
    f.close()
    



