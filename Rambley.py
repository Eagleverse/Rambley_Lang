###################################
#####        CONSTANTS        #####
###################################

DIGITS = '0123456789'  # digit
LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'  # ANY cap or lower -> tokens
MARK = print


###################################
#####         POSITION        #####
###################################
# Initialization of position, reading user inputs
class Position:
    def __init__(self, idx, ln, col):
        self.idx = idx
        self.ln = ln
        self.col = col

    # Advance method position
    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self


###################################
#####         TOKENS          #####
###################################
# Create Tokens (Token Type)
TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_ID = 'ID'
TT_KEYWORD = 'KEYWORD'
TT_EQ = 'EQ'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_EOF = 'EOF'

# Define Keywords
KEYWORDS = [
    'def', 'MARK', 'IF', 'ELSE', 'ENDIF', 'WHILE', 'ENDWHILE', 'DEPOSIT', 'WITHDRAWAL'
]


###################################
#####         LEXER           #####
###################################

# Initialize Tokens
class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    # Token's based off of this.
    def getType(self):
        return self.type

    def getVal(self):
        return self.value


# Initialize Lexer
class Lexer:
    def __init__(self, text):
        print("Running Lexer")
        self.text = text
        self.pos = Position(0, 0, 0)
        self.current_char = self.text[self.pos.idx]

    # Define advance, a method we use to move on to the next character
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    # Generate our tokens in regard to what characters represent them
    def generate_tokens(self):
        tokens = []

        while self.current_char is not None:
            # Ignore tab and space
            if self.current_char in ' \t':
                self.advance()
            # Identify DIGITS constant
            elif self.current_char in DIGITS:
                tokens.append(self.generate_number())
            # Identify LETTERS constant
            elif self.current_char in LETTERS:
                print("Letter")
                tokens.append(self.generate_identifier())
            # equals
            elif self.current_char == '=':
                tokens.append(Token(TT_EQ, self.current_char))
                self.advance()
            # plus
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, self.current_char))
                self.advance()
            # minus
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, self.current_char))
                self.advance()
            # Else, advance
            else:
                self.advance()
        # End of File, return tokens
        tokens.append(Token(TT_EOF, None))
        return tokens

    # Generate numbers, finding int if dot_count is 0 and float if dot_count is 1
    def generate_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char is not None and (self.current_char in DIGITS or self.current_char == '.'):
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
            num_str += self.current_char
            self.advance()
        # Return tokens
        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))

    # Generate identifiers which are either matching a keyword or an ID
    def generate_identifier(self):
        id_str = ''
        while self.current_char is not None and (self.current_char in LETTERS or self.current_char in DIGITS):
            id_str += self.current_char
            self.advance()
        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_ID
        return Token(tok_type, id_str)


###################################
#####         PARSER          #####
###################################

class ParseResult:
    def __init__(self):
        self.node = None
        self.error = None

    def register(self, res):
        if res.error:
            self.error = res.error
        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self


class MockNode:
    def __init__(self, value):
        self.kind = value


class IntNode:
    def __init__(self, value):
        self.kind = value


class FloatNode:
    def __init__(self, value):
        self.kind = value


class KWNode:
    def __init__(self, value):
        self.kind = value


class IDNode:
    def __init__(self, value):
        self.kind = value


class Parser:
    def __init__(self, tokens):
        print("Running Parser")
        self.tokens = tokens
        self.token_idx = 0
        self.current_token = self.tokens[self.token_idx]

    def advance(self):
        self.token_idx += 1
        if self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]

    def parse(self):
        if len(self.tokens) < 1:
            print(f"One input at a time, sorry!\nUsing your first input: {self.tokens[0]}")
        tok = self.tokens[0]
        res = ParseResult()
        print(tok.getType())
        #  node = MockNode()  # Replace this with actual parsing logic if needed
        if tok.getType() == "KEYWORD":
            node = KWNode(tok.getVal())
        elif tok.getType() == "ID":
            node = IDNode(tok.getVal())
        elif tok.getType() == "INT":
            node = IntNode(tok.getVal())
        elif tok.getType == "FLOAT":
            node = FloatNode(tok.getVal())
        else:
            node = MockNode(tok.getVal())
        return res.success(node)


###################################
#####      INTERPRETER        #####
###################################

class Interpreter:
    def visit(self, node):
        print("Running Interpreter")
        method_name = f'visit_{type(node).__name__}'
        print(method_name)
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_MockNode(self, node):
        return node

    def visit_KWNode(self, node):
        return node

    def visit_IDNode(self, node):
        return node

    def visit_IntNode(self, node):
        return node

    def visit_float(self, node):
        return node