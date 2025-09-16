class Evaluator:
    def __init__(self):
        self.variables = {}

    def evaluate(self, nodes):
        result = None
        for n in nodes:
            if isinstance(n, tuple) and n[0] == 'OUTPUT':
                value = self.evaluate_node(n[1])
                result = value
                print(value)
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
            print(self)
            return self.evaluate_node(node[1])
        elif node[0] == 'IF':
            condition  = self.evaluate_node(node[1])
            if condition:
                return self.evaluate(node[2]) if isinstance(node[2], list) else self.evaluate_node(node[2])
            elif node[3] is not None:
                return self.evaluate(node[3]) if isinstance(node[3],list) else self.evaluate_node(node[3])
            else: 
                return None
        elif node[0] in ('GREATER_THAN','LESS_THAN','EQUAL_TO','NOT_EQUAL_TO','GREATER_THAN_OR_EQUAL','LESS_THAN_OR_EQUAL'):
            left = self.evaluate_node(node[1])
            right = self.evaluate_node(node[2])
            if node[0] == 'GREATER_THAN':
                return left > right 
            if node[0] == 'LESS_THAN':
                return left < right
            if node[0] == 'EQUAL_TO':
                return left == right
            if node[0] == 'NOT_EQUAL_TO':
                return left != right
            if node[0] == 'GREATER_THAN_OR_EQUAL':
                return left >= right
            if node[0] == 'LESS_THAN_OR_EQUAL':
                return left <= right
        elif node[0] == 'ARRAY_ASSIGN':
            array_name, index_expr, value_expr = node[1], node[2], node[3]

            if array_name not in self.variables:
                raise Exception(f"Array {array_name} not declared")

            arr = self.variables[array_name]

            index = self.evaluate_node(index_expr)  # should be an int
            value = self.evaluate_node(value_expr)

            # Adjust if arrays declared as [1:n] but stored in Python as 0-indexed
            arr[index - 1] = value

            return value
        elif node[0] == 'INDEX':
            array_name, index_expr = node[1], node[2]

            if array_name not in self.variables:
                raise Exception(f"Array {array_name} not declared")

            arr = self.variables[array_name]

            index = self.evaluate_node(index_expr)
            return arr[index - 1]              
        elif node[0] == 'INPUT':
            var_name = node[1]
            value = input(f"{var_name}:")
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass
            self.variables[var_name] = value
            return value
        elif node[0] == 'FOR' : 
            var_name, start_expr, end_expr,body = node[1],node[2],node[3],node[4]
            start = self.evaluate_node(start_expr)
            end = self.evaluate_node(end_expr)
            
            #assign start to variable
            self.variables[var_name] = start
            while self.variables[var_name] <= end:
                self.evaluate(body)
                self.variables[var_name] += 1
            return None
        elif node[0] == 'WHILE':
            condition = node[1]
            body = node[2]
            while self.evaluate_node(condition):
                self.evaluate(body) if isinstance(body,list) else self.evaluate_node(body)

        elif node[0] == 'DECLARE':
            Identifier = node[1]
            DataType = node[2]

            if Identifier in self.variables:
                raise Exception(f"Variable {Identifier} already declared")

            # Handle ARRAY separately
            if isinstance(DataType, tuple) and DataType[0] == "ARRAY":
                bounds = DataType[1]      # e.g. [(1,5)] or [(1,3),(1,4)]
                element_type = DataType[2]

                # pick default based on element_type
                if element_type == "INTEGER_DTYPE":
                    default_value = 0
                elif element_type == "REAL_DTYPE":
                    default_value = 0.0
                elif element_type == "BOOLEAN_DTYPE":
                    default_value = False
                elif element_type == "STRING_DTYPE":
                    default_value = ""
                else:
                    raise Exception(f"Unknown array element type: {element_type}")

                # recursive initializer for multi-dimensional arrays
                def make_array(dim):
                    lower, upper = bounds[dim]
                    size = upper - lower + 1
                    if dim == len(bounds) - 1:  # last dimension
                        return [default_value for _ in range(size)]
                    else:
                        return [make_array(dim + 1) for _ in range(size)]

                self.variables[Identifier] = make_array(0)
                return f"declared {Identifier} as ARRAY{bounds} of {element_type}"

            # Scalar variable
            elif DataType == "INTEGER_DTYPE":
                self.variables[Identifier] = 0
            elif DataType == "REAL_DTYPE":
                self.variables[Identifier] = 0.0
            elif DataType == "BOOLEAN_DTYPE":
                self.variables[Identifier] = False
            elif DataType == "STRING_DTYPE":
                self.variables[Identifier] = ""
            else:
                raise Exception(f"Unknown data type: {DataType}")

            return f"declared {Identifier} as {DataType}"




        elif isinstance(node, str):  # IDENTIFIER
            return self.variables.get(node, 0)

        else:
            raise ValueError(f"Unknown AST node: {node}")
