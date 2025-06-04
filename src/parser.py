from src.ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.binary_operators = {
            "SUM_OF": "SUM OF",
            "DIFF_OF": "DIFF OF",
            "PRODUKT_OF": "PRODUKT OF",
            "QUOSHUNT_OF": "QUOSHUNT OF",
            "MOD_OF": "MOD OF",
            "BIGGR_OF": "BIGGR OF",
            "SMALLR_OF": "SMALLR OF",
            "BOTH_OF": "BOTH OF",
            "EITHER_OF": "EITHER OF",
            "WON_OF": "WON OF"
        }

    def current_token(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def match_token(self, *token_types):
        token = self.current_token()
        if token and token.type in token_types:
            self.position += 1
            return token
        return None

    def expect_token(self, token_type):
        token = self.match_token(token_type)
        if not token:
            current = self.current_token()
            line_info = f"at line {current.line}" if current else "at EOF"
            raise SyntaxError(f"Expected {token_type} {line_info}, but got {current.type if current else 'EOF'}")
        return token

    def parse(self):
        self.expect_token("HAI")
        statements = []
        while self.current_token() and self.current_token().type != "KTHXBYE":
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
        self.expect_token("KTHXBYE")
        return Program(statements)

    def parse_statement(self):
        token = self.current_token()
        if not token:
            return None

        handlers = {
            "VISIBLE": self.parse_visible,
            "I_HAS_A": self.parse_variable_declaration,
            "IDENTIFIER": self.parse_assignment,
            "IF": self.parse_if,
            "HOW": self.parse_function_definition,
            "I": self.parse_function_call,
            "FOUND": self.parse_return,
            "GTFO": self.parse_gtfo_statement,
        }

        handler = handlers.get(token.type)
        if handler:
            return handler()
        
        self.position += 1
        return NoOp()

    def parse_visible(self):
        self.expect_token("VISIBLE")
        return VisibleStatement(self.parse_expression())

    def parse_variable_declaration(self):
        self.expect_token("I_HAS_A")
        name = self.expect_token("IDENTIFIER").value
        value = None
        if self.match_token("ITZ"):
            value = self.parse_expression()
        return Assignment(name, value if value is not None else Literal(None))


    def parse_assignment(self):
        name = self.expect_token("IDENTIFIER").value
        self.expect_token("R")
        return Assignment(name, self.parse_expression())

    def parse_expression(self):
        token = self.current_token()
        if not token:
            raise SyntaxError("Unexpected end of input while parsing expression")

        if token.type in self.binary_operators:
            return self.parse_binary_operation()
        
        if token.type == "NUMBR":
            return Literal(int(self.match_token("NUMBR").value))
        
        if token.type == "STRING":
            return Literal(self.match_token("STRING").value.strip('"'))
        
        if token.type == "IDENTIFIER":
            return Variable(self.match_token("IDENTIFIER").value)
        
        raise SyntaxError(f"Unexpected token {token.type} at line {token.line} while parsing expression")

    def parse_binary_operation(self):
        operator_token = self.match_token(*self.binary_operators.keys())
        if not operator_token:
            raise SyntaxError(f"Expected a binary operator, but got {self.current_token().type if self.current_token() else 'EOF'}")
        
        operator_value = self.binary_operators[operator_token.type]
        left = self.parse_expression()
        self.expect_token("AN")
        right = self.parse_expression()
        return BinaryOperation(operator_value, left, right)

    def parse_if(self):
        self.expect_token("IF")
        self.expect_token("YA_RLY")
        
        true_block = self.parse_block_until(["NO_WAI", "OIC"])
        
        false_block = []
        if self.match_token("NO_WAI"):
            false_block = self.parse_block_until(["OIC"])
        
        self.expect_token("OIC")
        return IfStatement(Variable("IT"), true_block, false_block or None)

    def parse_block_until(self, terminators):
        statements = []
        while self.current_token() and self.current_token().type not in terminators:
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
        return statements

    def parse_function_definition(self):
        self.expect_token("HOW")
        self.expect_token("IZ")
        self.expect_token("I")
        name = self.expect_token("IDENTIFIER").value
        
        parameters = []
        while self.match_token("YR"):
            parameters.append(self.expect_token("IDENTIFIER").value)
            self.match_token("AN") 
        
        body = self.parse_block_until(["IF_U_SAY_SO"])
        self.expect_token("IF_U_SAY_SO")
        return FunctionDefinition(name, parameters, body)

    def parse_function_call(self):
        self.expect_token("I")
        self.expect_token("IZ")
        name = self.expect_token("IDENTIFIER").value
        
        arguments = []
        while self.match_token("YR"):
            arguments.append(self.parse_expression())
            self.match_token("AN") 
        
        self.expect_token("MKAY")
        return FunctionCall(name, arguments)

    def parse_return(self):
        self.expect_token("FOUND")
        self.expect_token("YR")
        return ReturnStatement(self.parse_expression())

    def parse_gtfo_statement(self):
        self.expect_token("GTFO")
        return ReturnStatement(Literal(None))