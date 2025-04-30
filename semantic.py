class Evaluator:
    def __init__(self):
        self.variables = {}

    def evaluate(self, nodes):
        result = None
        for n in nodes:
            result = self.evaluate_node(n)
            if isinstance(n, tuple) and n[0] == 'OUTPUT':
                value = self.evaluate_node(n[1])
                print("OUTPUT:", value)
            else:
                result = self.evaluate_node(n)
        return result
    
    def evaluate_node(self, node):
        if isinstance(node, int):
            return node

        if isinstance(node, tuple) and node[0] == 'STRING':
            return node[1]

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

        elif node[0] == 'OUTPUT':
            return self.evaluate_node(node[1])

        elif isinstance(node, str):  # IDENTIFIER
            return self.variables.get(node, 0)

        else:
            raise ValueError(f"Unknown AST node: {node}")
