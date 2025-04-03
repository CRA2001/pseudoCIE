class Evaluator:
    def __init__(self):
        self.variables = {}

    def evaluate(self, nodes):
        result = None
        for n in nodes:
            result = self.evaluate_node(n)  # Correct function call
        return result
    
    def evaluate_node(self, node):
        # Handle numbers directly
        if isinstance(node, int):
            return node

        if node[0] == 'ASSIGN':
            self.variables[node[1]] = self.evaluate_node(node[2])
            return self.variables[node[1]]

        elif node[0] == 'ADD':
            return self.evaluate_node(node[1]) + self.evaluate_node(node[2])  
        
        elif node[0] == 'SUB':
            return self.evaluate_node(node[1]) - self.evaluate_node(node[2]) 
        
        elif node[0] == 'MULTIPLY':
            return self.evaluate_node(node[1]) * self.evaluate_node(node[2])

        elif node[0] == 'DIVIDE':
            return self.evaluate_node(node[1]) / self.evaluate_node(node[2])

        # elif isinstance(node, tuple) and node[0] == 'IDENTIFIER':
        #     return self.variables.get(node[1], 0) 
        elif isinstance(node,str):
            return self.variables.get(node,0)

        else:
            raise ValueError(f"Unknown AST node: {node}")  
