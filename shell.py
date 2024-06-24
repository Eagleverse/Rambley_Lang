from Rambley import *


def run(text):
    lexer = Lexer(text)
    tokens = lexer.generate_tokens()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()
    result = interpreter.visit(ast.node)
    return result.kind


def main():
    text = ""
    while text.strip() != "exit()":
        text = input('BankS > ')
        if text.strip() == "":
            continue
        if text.strip() == "exit":
            break
        else:
            text = text.upper()
        result = run(text)
        print(result.kind)


# Execute the main function
if __name__ == "__main__":
    main()
