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

    #addition tests
    # print("TEST 1: 2 + 3")
    # code = "2 + 3"
    # run_code(code)

    # print("TEST 2: 2+3 ")
    # code = "2+3"
    # run_code(code)
    
    # print("TEST 3: 1+1+1")
    # code = "1+1+1"
    # run_code(code)

    # print("TEST 4: 1+2+3+4+5")
    # code = "1+2+3+4+5"
    # run_code(code)


    #TEST TO BREAK THE BOUNDARIES OF THE LANGUAGE: DO NOT UNCOMMENT THIS PLEASE
    # print("TEST 5: 1+2+3+...+1000")
    # code = "+".join(str(i) for i in range(1, 1001))  # Generates "1+2+3+...+1000"
    # run_code(code)

    # # print("TEST 1: 1-1")
    # code = "1 - 1"
    # run_code(code)
    # print("TEST 1: 100-1-1-2-3-4")
    # code = "100-1-1-2-3-4"
    # run_code(code)

    # #multiplication test:
    # print("TEST 1: 1 * 2 ")
    # code = "1*2"
    # run_code(code)
    # print("TEST 2: 1 * 2 * 3 ")
    # code = "1*2*3"
    # run_code(code)
    # print("TEST 2: 1 * 2 * 3  * 4 * 5")
    # code = "1 * 2 * 3 * 4 * 5"
    # run_code(code)

    # #divide test
    # print("TEST 1: 1/2 ")
    # code = "1/2"
    # run_code(code)
    # print("TEST 2: 24/4 ")
    # code = "24/4"
    # run_code(code)

<<<<<<< HEAD
    print("TEST 4: Multi-line Assignment")
    code = """
    x <- 1 + 1
    c <- x + 1
    """
    run_code(code)  # Should properly assign x and c
=======
    #Variables test
    print(" Test 1: x <- 1 ")
    code = "x <- 1"
    run_code(code)
    print(" Test 2: x <- 1+1")
    code = "x <- 1+1"
    run_code(code)
    print(" Test 3: x <- 1+1 \n c <- x + 1")
    code = '''
    x<-1+1
    c <- x + 1
    '''
    run_code(code)
    
>>>>>>> e17923a20ea9f245bab94680f5d8a4bdfc442c35
