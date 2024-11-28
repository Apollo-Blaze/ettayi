from lark import Lark, Tree, Token

# Assuming the parser and transformer are already set up correctly in the parser file.
import ettayi.parser as parser  # Your parser containing the Ettayi grammar and transformer

class EttayiInterpreter:
    def __init__(self):
        self.variables = {}
        self.executed = False
        self.if_executed = False  # Track if an 'if' has been executed

    def interpret(self, ast):
        if isinstance(ast, Tree) and ast.data == 'start':
            print("=====================================================================================")
            for statement in ast.children:
                if statement is not None:
                    self.execute(statement)  # Execute valid statements

    def execute(self, statement):
        """Execute a specific statement."""
        if isinstance(statement, tuple):
            op = statement[0]
            if op == "assign":
                self.assignment(statement[1], statement[2])
            elif op=="compound_assign":
                self.compound_assignment(statement[1:])
            elif op == "print_s":
                self.print_s(statement[1])
            elif op == "print_variable":
                self.print_variable(statement[1])
            elif op == "add":
                return statement[1] + statement[2]
            elif op == "subtract":
                return statement[1] - statement[2]
            elif op == "multiply":
                return statement[1] * statement[2]
            elif op == "divide":
                return statement[1] / statement[2]
            elif op == "while":
                condition, block = statement[1], statement[2]
                while self.evaluate_condition(condition):  
                    self.execute_block(block) 
            elif op == "for":
                var_name, start_value, end_value, block = statement[1], statement[2], statement[3], statement[4]
                if var_name not in self.variables:
                    self.variables[var_name] = start_value  # Initialize with the start value
                for i in range(start_value, end_value + 1):  # Execute for loop
                    self.variables[var_name] = i
                    self.execute_block(block)
            elif op == "if":
                self.executed = False
                if self.evaluate_condition(statement[1]):  
                    self.execute_block(statement[2])
                    self.executed = True
                self.if_executed = True
            elif op == "elif":
                if not self.if_executed:  # Raise error if no preceding 'if'
                    raise AssertionError("Error: 'elif' encountered without a preceding 'if'.")
                if not self.executed and self.evaluate_condition(statement[1]):  # Only check elif if no condition was met
                    self.execute_block(statement[2])
                    self.executed = True 
                    self.if_executed = False
            elif op == "else":
                if not self.if_executed and not self.executed:  # Raise error if no preceding 'if'
                    raise AssertionError("Error: 'else' encountered without a preceding 'if'.")
                if not self.executed:  # Only execute the else block if no if/elif was executed
                    self.else_statement(statement[1])
                    self.executed = False
                    self.if_executed = False
            elif op=="input":
                self.input_code(statement[1])
            else:
                raise Exception ("Error")
            
    def input_code(self,args):
        var_name=args
        user_input = input()
        if user_input.isdigit():
            value = int(user_input)  # Integer
        else:
            try:
                value = float(user_input)  # Float
            except ValueError:
                value = user_input  # String (fallback)
        # Assign the value to the variable
        self.variables[var_name] = value
        
            
    def compound_assignment(self, args):
        # Extract components of the assignment
        var_name_token = args[0]  # Variable name
        op = args[1]
        value_expr = args[2]  # Value expression

        # Ensure the variable exists
        var_name = var_name_token
        if var_name not in self.variables:
            raise NameError(f"Variable '{var_name}' is not defined. Declare it first using 'ivananu'.")

        # Evaluate the right-hand side expression
        value = self.evaluate_expression(value_expr)

        # Perform the compound operation
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
        elif op == "assign":  # Overwrite assignment
            self.variables[var_name] = value
        else:
            raise ValueError(f"Unsupported compound operation: {op}")
        
    def evaluate_expression_new(self, expr):

        if isinstance(expr, Tree):
            if len(expr.children) == 2:  # Binary operations (like comparisons, arithmetic)
                op = expr.data
                left = self.evaluate_expression_new(expr.children[0].children[0])
                right = self.evaluate_expression_new(expr.children[1].children[0])

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
                else:
                    raise ValueError(f"Unsupported binary operation: {op}")

            elif len(expr.children) == 1:  # Parentheses or single value
                return self.evaluate_expression_new(expr.children[0])

            else:
                raise ValueError(f"Unexpected tree structure: {expr}")
        
        elif isinstance(expr, Token):
            if expr.type == "NUMBER":
                # Check if the number has a decimal point (float) or not (integer)
                if '.' in expr.value:
                    return float(expr.value)
                else:
                    return int(expr.value)
            elif expr.type == "STRING":
                return expr.value[1:-1]  # Remove quotes from string value
            elif expr.type == "IDENTIFIER":
                # Handle variables (IDENTIFIER tokens)
                if expr.value in self.variables:
                    return self.variables[expr.value]
                else:
                    raise NameError(f"Variable '{expr.value}' is not defined")
            else:
                raise ValueError(f"Unsupported token type: {expr.type}")
        
        else:
            raise ValueError(f"Unsupported node type: {expr}")

    
    def evaluate_condition(self, condition):
        if isinstance(condition, bool):
            return condition
        elif isinstance(condition, Tree):  # Condition is a Tree (comparison)
            fin = self.evaluate_expression_new(condition)
            return (fin)

            

    
    def execute_block(self, block):
        for statement in block.children:
            self.execute(statement)
                
    def if_statement(self, block):
        """Execute an 'if' block."""
        if block:
            for statement in block.children:
                self.execute(statement)
            return True

    def elif_statement(self, block):
        if block:
            for statement in block.children:  # Access the children of the Tree
                self.execute(statement)
            return True

    def else_statement(self, block):
        """Execute an 'else' block."""
        if block:
            for statement in block.children:
                self.execute(statement)
            return True

    def assignment(self, var_name, value):
        if isinstance(value, Token):
            if value.type == 'BOOLEAN':
                self.variables[var_name] = value.value == "sheri"
            elif value.type == 'NUMBER':
                self.variables[var_name] = float(value.value)
            elif value.type == 'STRING':
                self.variables[var_name] = value.value[1:-1]  # Remove quotes
            elif value.type == 'IDENTIFIER':
                if value.value in self.variables:
                    self.variables[var_name] = self.variables[value.value]
                else:
                    raise NameError(f"Variable '{value.value}' is not defined")
        elif isinstance(value, Tree):
            self.variables[var_name] = self.evaluate_expression(value)
        else:
            self.variables[var_name] = value

    def print_s(self, string):
        """Print a string."""
        print(string)

    def print_variable(self, var_name):
        """Print the value of a variable."""
        if var_name in self.variables:
            print(self.variables[var_name])
        else:
            print(f"Error: {var_name} is not defined")

    
    def evaluate_expression(self, expr):
        if isinstance(expr, Tree):
            op = expr.data  # Get the operation type (add, subtract, etc.)
            if op == 'add':
                return self.evaluate_expression(expr.children[0]) + self.evaluate_expression(expr.children[1])
            elif op == 'subtract':
                return self.evaluate_expression(expr.children[0]) - self.evaluate_expression(expr.children[1])
            elif op == 'multiply':
                return self.evaluate_expression(expr.children[0]) * self.evaluate_expression(expr.children[1])
            elif op == 'divide':
                return self.evaluate_expression(expr.children[0]) / self.evaluate_expression(expr.children[1])
            elif op == 'number':
                return float(expr.children[0])  # Directly return the number
            elif op == 'variable':
                var_name = str(expr.children[0])  # Should be an identifier
                if var_name in self.variables:
                    return self.variables[var_name]
                raise NameError(f"Variable '{var_name}' is not defined")
        elif isinstance(expr, Token):
            if expr.type == 'NUMBER':
                return float(expr.value)  # Return the number value
            elif expr.type == 'STRING':
                return expr.value[1:-1]  # Return the string value, removing quotes
            elif expr.type == 'BOOLEAN':
                return expr.value == 'sheri'  # Custom condition, adjust as needed
        elif isinstance(expr, (int, float)):
            return expr  # Return the value if it's a number
        elif isinstance(expr, str):
            return expr  # Return the string as is
        else:
            raise ValueError(f"Unsupported expression: {expr}")
        
def execute_ettayi_file(filename):
    # Read the .ettayi file content
    with open(filename, 'r', encoding='utf-8') as file:
        ettayi_code = file.read()

    # Parse and execute the code
    try:
        parser = Lark(parser.ettayi_grammar, parser="lalr", transformer=parser.EttayiTransformer())
        tree = parser.parse(ettayi_code)  # Parse the file
        print("Execution finished successfully.")
    except Exception as e:
        print(f"Error while executing {filename}: {e}")


# Initialize the interpreter and parser
if __name__ == "__main__":
    # Ensure you import the Ettayi grammar and transformer from your parser file
    parser = Lark(parser.ettayi_grammar, parser="lalr", transformer=parser.EttayiTransformer())
    interpreter = EttayiInterpreter()

    code = '''
    "Hello ettayi sugalle" para;

ivananu a = 5;
ivananu b = 10;
ivananu sum = a + b;

"The sum of a and b is:" para;
sum para;

"Enter a number:" para;
user_input choik;
"You entered:" para;
user_input para;

anenki (user_input > sum) {
    "Your number is greater than the sum." para;
} allenki (user_input < sum) {
    "Your number is less than the sum." para;
} avasanam {
    "Your number is equal to the sum." para;
}

"Looping through numbers:" para;
ithinulil (i = 1..5) {
    i para;
}

ivananu count = 0;

cheyuka (count < 3) {
    "Current count:" para;
    count para;
    count += 1;
}

ivananu x = 10;
x += 5;
"The value of x after incrementing is:" para;
x para;

    '''


    # Parse the code using the Ettayi parser
    ast = parser.parse(code)
    print(f"Generated AST: {ast}")

    # Execute the parsed AST with the interpreter
    interpreter.interpret(ast)
