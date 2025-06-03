from src.ast_nodes import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def match(self, *token_types):
        token = self.current()
        if token and token.type in token_types:
            self.pos += 1
            return token
        return None

    def expect(self, token_type):
        token = self.match(token_type)
        if not token:
            current = self.current()
            raise SyntaxError(f"Expected {token_type} at line {current.line if current else 'EOF'}")
        return token

    def parse(self):
        self.expect("HAI")
        statements = []
        while self.current() and self.current().type != "KTHXBYE":
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        self.expect("KTHXBYE")
        return Program(statements)

    def parse_statement(self):
        token = self.current()
        if not token:
            return None

        if token.type == "VISIBLE":
            return self.parse_visible()
        elif token.type == "I_HAS_A":
            return self.parse_variable_declaration()
        elif token.type == "IDENTIFIER":
            return self.parse_assignment()
        elif token.type == "IF":
            return self.parse_if()
        else:
            self.pos += 1
            return NoOp()

    def parse_visible(self):
        self.expect("VISIBLE")
        expr = self.parse_expression()
        return VisibleStatement(expr)

    def parse_variable_declaration(self):
        self.expect("I_HAS_A")
        var_name = self.expect("IDENTIFIER").value
        if self.match("ITZ"):
            value_expr = self.parse_expression()
        else:
            value_expr = Literal(None)
        return Assignment(var_name, value_expr)

    def parse_assignment(self):
        var_name = self.expect("IDENTIFIER").value
        self.expect("R")
        value_expr = self.parse_expression()
        return Assignment(var_name, value_expr)

    def parse_expression(self):
        token = self.current()

        if token.type in ("SUM_OF", "DIFF_OF", "PRODUKT_OF", "QUOSHUNT_OF", "MOD_OF",
                          "BIGGR_OF", "SMALLR_OF", "BOTH_OF", "EITHER_OF", "WON_OF"):
            op_token = self.match(token.type)
            left = self.parse_expression()
            self.expect("AN")
            right = self.parse_expression()
            return BinaryOperation(op_token.type.replace("_", " "), left, right)

        elif token.type == "NUMBR":
            return Literal(int(self.match("NUMBR").value))
        elif token.type == "STRING":
            value = self.match("STRING").value
            return Literal(value.strip('"'))
        elif token.type == "IDENTIFIER":
            return Variable(self.match("IDENTIFIER").value)
        else:
            raise SyntaxError(f"Unexpected token {token.type} at line {token.line}")

    def parse_if(self):
        self.expect("IF")
        true_block = []
        false_block = []
        self.expect("YA_RLY")
        while self.current() and self.current().type not in ("NO_WAI", "OIC"):
            stmt = self.parse_statement()
            if stmt:
                true_block.append(stmt)
        if self.match("NO_WAI"):
            while self.current() and self.current().type != "OIC":
                stmt = self.parse_statement()
                if stmt:
                    false_block.append(stmt)
        self.expect("OIC")
        return IfStatement(Variable("IT"), true_block, false_block or None)
