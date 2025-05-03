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
    print("TEST 1: OUTPUT Hello World")
    code = '''
    OUTPUT "Hello World"
    '''
    run_code(code)
    print("*" * 20)

    print("TEST 2 : OUTPUT 1")
    code = '''
    OUTPUT 1
    '''
    run_code(code)
    print("*" * 20)
    print("TEST 3 : OUTPUT with variables")
    code = '''
    a <- 3
    b <- 4
    OUTPUT a + b
    '''
    run_code(code)
    print("*" * 20)
    print("TEST 4 : Break this shit")
    code = '''
    a <- 999999999999999999
    b <- 999999999999999999
    OUTPUT a + b  
    '''
    run_code(code)
    with open("ExternalTest.txt",'r') as f:
        code = f.read()
        print(code)
        run_code(code)
    f.close()
    



