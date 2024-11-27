from lark import Lark, Transformer

# Ettayi Language grammar with the new 'ivan' keyword for assignments
ettayi_grammar = r"""
    start: statement+

    // Statements
    statement: "para" "(" STRING ")" ";"              -> print_statement
             | "para" "(" IDENTIFIER ")" ";"          -> print_variable
             | "para" "(" expression ")" ";"          -> print_all
             | "ivan" IDENTIFIER "=" expression ";"   -> assignment      // 'ivan' for assignment
             | "anenki" "(" condition ")" block       -> if_statement
             | "illel" "(" condition ")" block        -> elif_statement
             | "illenkil" block                       -> else_statement
             | "ithanenki" "(" condition ")" block    -> while_loop
             | "ithinulil" "(" IDENTIFIER "=" INT ".." INT ")" block -> for_loop

    // Expressions
    expression: term
              | expression "+" term                   -> add
              | expression "-" term                   -> subtract

    term: factor
         | term "*" factor                        -> multiply
         | term "/" factor                        -> divide

    factor: NUMBER                                -> number
          | STRING                                -> string
          | IDENTIFIER                            -> variable
          | "(" expression ")"                   -> parens

    // Conditions
    condition: IDENTIFIER ">" NUMBER                 -> greater_than
             | IDENTIFIER "<" NUMBER                 -> less_than
             | IDENTIFIER ">=" NUMBER                -> greater_or_equal
             | IDENTIFIER "<=" NUMBER                -> less_or_equal
             | IDENTIFIER "==" NUMBER                -> equal
             | IDENTIFIER "!=" NUMBER                -> not_equal

    // Blocks
    block: "{" statement+ "}"

    // Tokens
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
    
    def print_all(self,args):
        print(args)

    def print_statement(self, args):
        return ("print_s", args[0][1:-1])  # Remove quotes from the string

    def print_variable(self, args):
        var_name = str(args[0])
        return ("print", var_name)

    def assignment(self, args):
        var_name = str(args[0])
        value = args[1]
        # Handle assignment for both literals and expressions
        if isinstance(value,tuple):
            print(value)
            print(self.evaluate_expression(value))
            print("Tes")
        elif isinstance(value.children[0].children[0], str):
            if value.children[0].children[0][0]!='"' or value.children[0].children[0][0]!="'":
                self.variables[var_name]=self.variables[value.children[0].children[0]]
                return ("assign",var_name,self.variables[value.children[0].children[0]])

        elif isinstance(value.children[0].children[0], (int, float)):  # Direct number assignment
            self.variables[var_name] = value
        else:  # Expression assignment
            self.variables[var_name] = self.evaluate_expression(value)
        return ("assign", var_name, self.variables[var_name])

    def evaluate_expression(self, expr):
        """Evaluate an expression."""
        print(expr)
        if isinstance(expr, tuple):
            
            
            op = expr[0]
            if op == "add":
                return self.evaluate_expression(expr[1]) + self.evaluate_expression(expr[2])
            elif op == "subtract":
                return self.evaluate_expression(expr[1]) - self.evaluate_expression(expr[2])
            elif op == "multiply":
                return self.evaluate_expression(expr[1]) * self.evaluate_expression(expr[2])
            elif op == "divide":
                return self.evaluate_expression(expr[1]) / self.evaluate_expression(expr[2])
            else:
                return expr  # In case of simple number or variable
        return expr

    def if_statement(self, args):
        return ("if", args[0], args[1])

    def elif_statement(self, args):
        return ("elif", args[0], args[1])

    def else_statement(self, args):
        return ("else", args[0])

    def while_loop(self, args):
        return ("while", args[0], args[1])

    def for_loop(self, args):
        return ("for", str(args[0]), int(args[1]), int(args[2]), args[3])

    def greater_than(self, args):
        return ("greater_than", str(args[0]), int(args[1]))

    def less_than(self, args):
        return ("less_than", str(args[0]), int(args[1]))

    def greater_or_equal(self, args):
        return ("greater_or_equal", str(args[0]), int(args[1]))

    def less_or_equal(self, args):
        return ("less_or_equal", str(args[0]), int(args[1]))

    def equal(self, args):
        return ("equal", str(args[0]), int(args[1]))

    def not_equal(self, args):
        return ("not_equal", str(args[0]), int(args[1]))

    def add(self, args):
        return ("add", args[0], args[1])

    def subtract(self, args):
        return ("subtract", args[0], args[1])

    def multiply(self, args):
        return ("multiply", args[0], args[1])

    def divide(self, args):
        return ("divide", args[0], args[1])

    def number(self, args):
        return float(args[0])

    def string(self, args):
        return str(args[0][1:-1])  # Remove quotes from string

    def variable(self, args):
        return str(args[0])

    def parens(self, args):
        return args[0]

    def block(self, args):
        return args

# Create the parser
parser = Lark(ettayi_grammar, parser="lalr", transformer=EttayiTransformer())

if __name__ == "__main__":
    # Example code in Ettayi Language using 'ivan' for assignment
    code = '''
    para("Starting language test");
    ivan x=5;
    ivan y=4;
    ivan ay=6;
    ivan z=ay;
    para(z);
    '''
    
    # Parse the code
    ast = parser.parse(code)
    print(ast.pretty())  # Print the parse tree for debugging
