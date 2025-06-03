class ASTNode:
    def __repr__(self):
        attrs = ', '.join(f"{key}={repr(value)}" for key, value in self.__dict__.items() if not key.startswith('_'))
        return f"{self.__class__.__name__}({attrs})"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.__dict__ == other.__dict__

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements


class VisibleStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression


class Literal(ASTNode):
    def __init__(self, value):
        self.value = value


class Variable(ASTNode):
    def __init__(self, name):
        self.name = name


class Assignment(ASTNode):
    def __init__(self, variable_name, value_expr):
        self.variable_name = variable_name
        self.value_expr = value_expr


class BinaryOperation(ASTNode):
    def __init__(self, operator, left, right):
        self.operator = operator  # e.g., "SUM OF", "DIFF OF"
        self.left = left
        self.right = right


class IfStatement(ASTNode):
    def __init__(self, condition, true_block, false_block=None):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block


class Loop(ASTNode):
    def __init__(self, variable_name, start_expr, end_expr, body):
        self.variable_name = variable_name
        self.start_expr = start_expr
        self.end_expr = end_expr
        self.body = body


class NoOp(ASTNode):
    pass
