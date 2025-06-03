import sys
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter


def main():
    if len(sys.argv) != 2:
        print("Usage: python src/main.py <path_to_lolcode_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        with open(file_path, 'r') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)

    try:
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()


        interpreter = Interpreter()
        interpreter.interpret(ast)

    except SyntaxError as e:
        print(f"Syntax error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Runtime error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

