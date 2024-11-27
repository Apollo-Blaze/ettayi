from lark import Lark, Tree
import parser  # Assuming you already have parser.py with the grammar and transformer

class EttayiInterpreter:
    def __init__(self):
        self.variables = {}

    def interpret(self, ast, draw=True):
        print(ast)
        print(ast.children)
        print("=======================================================================================")

        # The statements are in the first child of the 'start' node.
        if isinstance(ast, Tree) and ast.data == 'start':
            executed = False  # To track if any condition has been met
            for statement in ast.children:
                if isinstance(statement, tuple):
                    op = statement[0]
                    if op == "if" and not executed:
                        executed = self.if_statement(statement[1], statement[2])
                    elif op == "elif" and not executed:
                        executed = self.elif_statement(statement[1], statement[2])
                    elif op == "else" and not executed:
                        self.else_statement(statement[1])
                    else:
                        self.execute(statement)

    def execute(self, statement):
        if isinstance(statement, tuple):
            op = statement[0]
            if op == "assign":
                self.assignment(statement[1], statement[2])
            elif op == "print_s":
                self.print_s(statement[1])
            elif op == "print":
                self.print_variable(statement[1])
            elif op == "while":
                self.while_loop(statement[1], statement[2])
            elif op == "for":
                self.for_loop(statement[1], statement[2], statement[3], statement[4])
            elif op == "add":
                return statement[1] + statement[2]
            elif op == "subtract":
                return statement[1] - statement[2]
            elif op == "multiply":
                return statement[1] * statement[2]
            elif op == "divide":
                return statement[1] / statement[2]

    def assignment(self, var_name, value):
        """Assign a value to a variable."""
        if isinstance(value, Tree) and value.data == 'expression':
            evaluated_value = value.children[0].children[0]  # Extract the first term's first child (numeric value)
            self.variables[var_name] = evaluated_value
        else:
            self.variables[var_name] = value
    
    def print_s(self, string):
        return print(string)

    def print_variable(self, var_name):
        """Print the value of a variable."""
        if var_name in self.variables:
            print(self.variables[var_name])
        else:
            print(f"Error: {var_name} is not defined")

    def if_statement(self, condition, blocks):
        """Execute a block of code if the condition is True."""
        if self.evaluate_condition(condition):
            for block in blocks:
                self.execute(block)
            return True  # Indicate that the block has been executed
        return False  # Indicate that the block was not executed

    def elif_statement(self, condition, blocks):
        """Execute a block of code if the 'if' condition was False and this condition is True."""
        if self.evaluate_condition(condition):
            for block in blocks:
                self.execute(block)
            return True  # Indicate that the block has been executed
        return False  # Indicate that the block was not executed

    def else_statement(self, blocks):
        """Execute the block of code in the 'else' section."""
        for block in blocks:
            self.execute(block)

    def while_loop(self, condition, blocks):
        """Execute a block of code while the condition is True."""
        while self.evaluate_condition(condition):
            for block in blocks:
                print(block)
                self.execute(block)

    def for_loop(self, var_name, start, end, blocks):
        """Execute a block of code for a range of values."""
        for i in range(start, end + 1):
            self.variables[var_name] = i
            for block in blocks:
                print(block)
                self.execute(block)

    def evaluate_condition(self, condition):
        """Evaluate a condition expression."""
        op = condition[0]
        var_name = condition[1]
        number = condition[2]

        if op == "greater_than":
            return self.variables.get(var_name, 0) > number
        elif op == "less_than":
            return self.variables.get(var_name, 0) < number
        elif op == "greater_or_equal":
            return self.variables.get(var_name, 0) >= number
        elif op == "less_or_equal":
            return self.variables.get(var_name, 0) <= number
        elif op == "equal":
            return self.variables.get(var_name, 0) == number
        elif op == "not_equal":
            return self.variables.get(var_name, 0) != number
        return False

# Initialize the interpreter and parser
if __name__ == "__main__":
    # Ensure you import the Ettayi grammar and transformer from your parser file
    parser = Lark(parser.ettayi_grammar, parser="lalr", transformer=parser.EttayiTransformer())
    interpreter = EttayiInterpreter()

    code = '''
    para("Starting language test");
    ivan x=5;
    ivan y=4;
    ivan ay=6;
    ivan z=y;
    para(z);
    ivan a=6;
    para(a);
    '''

    # Parse the code using the Ettayi parser
    ast = parser.parse(code)
    
    # Execute the parsed AST with the interpreter
    interpreter.interpret(ast)
