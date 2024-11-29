from lark import Lark, Transformer, Token, Tree

# Ettayi Language grammar
ettayi_grammar = r"""
    start: statement+

    // Statements
    statement: STRING "para" ";"                           -> print_statement
             | IDENTIFIER "para" ";"                       -> print_variable
             | expression "para" ";"                       -> print_all
             | "ivananu" IDENTIFIER "=" expression ";"     -> assignment
             | IDENTIFIER compound_op expression ";"       -> compound_assignment
             | "sathyavastha" IDENTIFIER "=" sathyavastha_value ";" -> boolean_assignment
             | "anenki" "(" condition ")" block            -> if_statement
             | "allenki" "(" condition ")" block             -> elif_statement
             | "avasanam" block                            -> else_statement
             | "cheyuka" "(" condition ")" block         -> while_loop
             | "ithinulil" "(" IDENTIFIER "=" INT ".." INT ")" block -> for_loop
             | IDENTIFIER "choik" ";"                      -> input_statement

    compound_op: "+=" -> add
               | "-=" -> subtract
               | "*=" -> multiply
               | "/=" -> divide
               | "%=" -> modulo
               | "=" -> assign

    // Expressions
    expression: term
              | expression "+" term                    -> add
              | expression "-" term                    -> subtract

    term: factor
         | term "*" factor                            -> multiply
         | term "/" factor                            -> divide

    factor: NUMBER                                     -> number
          | STRING                                     -> string
          | IDENTIFIER                                 -> variable
          | "(" expression ")"                        -> parens

    // Conditions
    condition: comparison
         | comparison ">" comparison     -> greater_than
         | comparison "<" comparison     -> less_than
         | comparison ">=" comparison    -> greater_or_equal
         | comparison "<=" comparison    -> less_or_equal
         | comparison "==" comparison    -> equal
         | comparison "!=" comparison    -> not_equal

        comparison: IDENTIFIER
                | NUMBER
    // Blocks
    block: "{" statement+ "}"

    // Tokens
    sathyavastha_value: "sheri"   -> sheri
                       | "thettu" -> thettu
    STRING: /".*?"/
    IDENTIFIER: /[a-zA-Z_][a-zA-Z0-9_]*/
    INT: /[0-9]+/
    NUMBER: /[0-9]+(\.[0-9]+)?/
    %import common.WS
    %ignore WS
"""

# Parse tree transformer
class EttayiTransformer(Transformer):
    def __init__(self):
        self.variables = {}
    
    def input_statement(self, args):
        var_name = str(args[0])  # Extract the variable name
        self.variables[var_name]=0
        return ("input",var_name)

    def print_statement(self, args):
        return ("print_s",args[0][1:-1])  # Remove quotes and print

    def print_variable(self, args):
        var_name = str(args[0])
        return ("print_variable",var_name)

    def print_all(self, args):
        return ("print_s",self.evaluate_expression(args[0]))

    def assignment(self, args):
        var_name = str(args[0])
        value = self.evaluate_expression(args[1])
        self.variables[var_name] = value
        return ("assign", var_name, value)

    def compound_assignment(self, args):
        var_name = str(args[0])
        op = args[1].data  # Extract the operation type
        value = self.evaluate_expression(args[2])
        if var_name not in self.variables:
            raise NameError(f"Variable '{var_name}' is not defined. Declare it first using 'ivananu'.")

        if op == "add":
            self.variables[var_name] += value
        elif op == "subtract":
            self.variables[var_name] -= value
        elif op == "multiply":
            self.variables[var_name] *= value
        elif op == "divide":
            self.variables[var_name] /= value
        elif op == "modulo":
            self.variables[var_name] %= value
        if op == "assign":
            self.variables[var_name] = value

        return ("compound_assign", var_name,op, value)

    def boolean_assignment(self, args):
        var_name = str(args[0])
        value = args[1].data  # 'sheri' or 'thettu'
        self.variables[var_name] = (value == "sheri")
        return ("boolean_assign", var_name, value)

    def evaluate_expression(self, expr):
        if isinstance(expr, Tree):
            if len(expr.children) == 2:  # Binary operation (like comparisons)
                op = expr.data
                left = self.evaluate_expression(expr.children[0])
                right = self.evaluate_expression(expr.children[1])

                if op == "add":
                    return left + right
                elif op == "subtract":
                    return left - right
                elif op == "multiply":
                    return left * right
                elif op == "divide":
                    return left / right
                elif op == "greater_than":
                    return left > right
                elif op == "less_than":
                    return left < right
                elif op == "greater_or_equal":
                    return left >= right
                elif op == "less_or_equal":
                    return left <= right
                elif op == "equal":
                    return left == right
                elif op == "not_equal":
                    return left != right
            elif len(expr.children) == 1:  # Parentheses or single value
                return self.evaluate_expression(expr.children[0])
            else:
                raise ValueError(f"Unexpected tree structure: {expr}")
        elif isinstance(expr, Token):
            if expr.type == "NUMBER":
                if '.' in expr.value:  # Check if the number has a decimal point
                    return float(expr.value)
                else:
                    return int(expr.value)
            elif expr.type == "INT":
                return int(expr.value)
            elif expr.type == "STRING":
                return expr.value[1:-1]  # Remove quotes
            elif expr.type == "IDENTIFIER":
                if expr.value in self.variables:
                    return self.variables[expr.value]
                else:
                    raise NameError(f"Variable '{expr.value}' is not defined")
        else:
            raise ValueError(f"Unsupported node type: {expr}")
    
    # The rest of the code remains unchanged...


    def if_statement(self, args):
        condition = args[0]  # Evaluate the condition
        block=args[1]
        return("if",condition,block)

    def elif_statement(self, args):
        condition = args[0]  # Evaluate the condition
        block=args[1]
        return("elif",condition,block)

    def else_statement(self, args):
        return ("else", args[0])  # Execute the 'else' block

    def execute_block(self, block):
        result = []
        for statement in block.children:
            if isinstance(statement, Tree):
                result.append(self.transform(statement))  
        return result
    
    def while_loop(self, args):
        condition = (args[0])  # Evaluate the condition
        block = args[1]  # The block of statements to execute
        return ("while", condition, block)

    def for_loop(self, args):
        var_name = str(args[0])  # The loop variable (e.g., x in x=1..10)
        start_value = self.evaluate_expression(args[1]) 
        end_value = self.evaluate_expression(args[2])  # End value (e.g., 10)
        block = args[3]  # The block of statements to execute for each iteration
        return ("for", var_name, start_value, end_value, block)  # Return the loop details


# Create the parser
parser = Lark(ettayi_grammar, parser="lalr", transformer=EttayiTransformer())

# Example code in Ettayi Language
if __name__ == "__main__":
    code = '''
    a choik;
    anenki(a<9){
        a +=1 ;
    }

    '''

    parser.parse(code)