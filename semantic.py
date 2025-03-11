class Evaluator:
    def evaluate(self,node):
        if node[0] == 'ADD':
            return node[1] + node[2]