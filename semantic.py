class Evaluator:
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
        else:
            return node
