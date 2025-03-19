class Evaluator:
    def __init__(self):
        self.variables = {}

    def evaluate(self,node):
        #using recursion to handle nested tuples 😡
        if isinstance(node,tuple):
            if node[0] == 'ADD':
                return self.evaluate(node[1]) + self.evaluate(node[2]) #recursively evualate
            elif node[0] == 'SUB':
                return self.evaluate(node[1]) - self.evaluate(node[2]) 
            elif node[0] == 'MULTIPLY':
                return self.evaluate(node[1]) * self.evaluate(node[2])
            elif node[0] == 'DIVIDE':
                return self.evaluate(node[1]) / self.evaluate(node[2])
            elif node[0] == 'ASSIGN':
                var_name = node[1]
                value = self.evaluate(node[2])
                self.variables[var_name] = value
            return value 
        elif isinstance(node,str):
            if node in self.variables: 
                return self.variables[node]
            else: 
                NameError(f"Variable '{node}' is not defined")
        else:
            return node
