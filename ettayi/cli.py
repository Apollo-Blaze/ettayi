import argparse
import sys
from interpreter import EttayiInterpreter
from parser import ettayi_grammar  # Import your grammar here
import parser as parserr
from lark import Lark

def main():
    parser = argparse.ArgumentParser(description="Run Ettayi Language programs.")
    parser.add_argument("filename", type=str, help="Path to the .ettayi file to execute.")
    args = parser.parse_args()

    # Read the file
    try:
        with open(args.filename, 'r', encoding='utf-8') as file:
            code = file.read()
    except FileNotFoundError:
        print(f"Error: File '{args.filename}' not found.")
        sys.exit(1)

    # Parse and interpret the code
    try:
        # Initialize the parser and interpreter
        parser = Lark(ettayi_grammar, parser="lalr", transformer=parserr.EttayiTransformer())
        interpreter = EttayiInterpreter()
        ast = parser.parse(code)
        interpreter.interpret(ast)
        print("=====================================================================================")
    except Exception as e:
        print(f"Error during execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
