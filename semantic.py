class Evaluator:
    def __init__(self):
        self.variables = {}
<<<<<<< HEAD
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
=======

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
>>>>>>> e17923a20ea9f245bab94680f5d8a4bdfc442c35
        else:
            return node

