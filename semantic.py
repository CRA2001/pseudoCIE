class Evaluator:
    def __init__(self):
        self.variables = {}
    def evaluate(self,nodes):
        result = None
        for n in nodes:
            result = self.evaluate_node(n)
        return result
    def evaluate_node(self,node):
        #using recursion to handle nested tuples 😡
        if node[0] == 'ASSIGN':
            self.variables[node[1]] = self.evaluate_node(node[2])
            return self.variables[node[1]]
        elif node[0] == 'ADD':
            return self.evaluate(node[1]) + self.evaluate(node[2]) #recursively evualate
        elif node[0] == 'SUB':
            return self.evaluate(node[1]) - self.evaluate(node[2]) 
        elif node[0] == 'MULTIPLY':
            return self.evaluate(node[1]) * self.evaluate(node[2])
        elif node[0] == 'DIVIDE':
            return self.evaluate(node[1]) / self.evaluate(node[2]) 
        elif isinstance(node,tuple) and node[0] == 'IDENTIFIER':
            return self.variables.get(node[1],0)
        else:
            return node

