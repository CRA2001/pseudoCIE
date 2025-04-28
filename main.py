#importing all the other parts of the compiler
from lexer import Lexer
from parser import Parser
from semantic import Evaluator

def run_code(code):
    #step 1: tokenize the code
    lexer = Lexer(code)
    tokens=lexer.tokenize()
    print("Tokens: ", tokens)

    #step 2: parse tokens into AST
    parser = Parser(tokens)
    ast = parser.parse()
    print("AST: ", ast)

    #step 3: evaluate the AST to get resule
    evaluator = Evaluator()
    result = evaluator.evaluate(ast)
    print("RESULT: ", result)


if __name__ == '__main__':
    code = '''
    OUTPUT "Hello World"
    '''
    run_code(code)