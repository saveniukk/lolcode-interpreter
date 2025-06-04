from src.ast_nodes import *


class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.functions = {}
        self.parent = parent

    def set(self, name, value):
        self.variables[name] = value

    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise NameError(f"Variable '{name}' not defined")

    def define_function(self, name, parameters, body):
        self.functions[name] = (parameters, body)

    def get_function(self, name):
        if name in self.functions:
            return self.functions[name]
        elif self.parent:
            return self.parent.get_function(name)
        else:
            raise NameError(f"Function '{name}' not defined")

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class Interpreter:
    def __init__(self):
        self.env = Environment()

    def interpret(self, node):
        if isinstance(node, Program):
            for stmt in node.statements:
                self.interpret(stmt)

        elif isinstance(node, VisibleStatement):
            value = self.evaluate(node.expression)
            print(value)

        elif isinstance(node, Assignment):
            value = self.evaluate(node.value_expr)
            self.env.set(node.variable_name, value)

        elif isinstance(node, IfStatement):
            condition = self.evaluate(node.condition)
            if condition:
                for stmt in node.true_block:
                    self.interpret(stmt)
            elif node.false_block:
                for stmt in node.false_block:
                    self.interpret(stmt)

        elif isinstance(node, Loop):
            start = self.evaluate(node.start_expr)
            end = self.evaluate(node.end_expr)
            for i in range(start, end + 1):
                self.env.set(node.variable_name, i)
                for stmt in node.body:
                    self.interpret(stmt)

        elif isinstance(node, FunctionDefinition):
            self.env.define_function(node.name, node.parameters, node.body)

        elif isinstance(node, ReturnStatement):
            value = self.evaluate(node.expression)
            raise ReturnException(value)

        elif isinstance(node, NoOp):
            pass

        else:
            raise Exception(f"Unsupported node type: {type(node).__name__}")

    def evaluate(self, expr):
        if isinstance(expr, Literal):
            return expr.value

        elif isinstance(expr, Variable):
            return self.env.get(expr.name)

        elif isinstance(expr, BinaryOperation):
            left = self.evaluate(expr.left)
            right = self.evaluate(expr.right)
            return self._apply_operator(expr.operator, left, right)

        elif isinstance(expr, FunctionCall):
            func = self.env.get_function(expr.name)
            if func is None:
                raise NameError(f"Function '{expr.name}' not defined")
            parameters, body = func
            if len(parameters) != len(expr.arguments):
                raise Exception(f"Function '{expr.name}' expects {len(parameters)} arguments, got {len(expr.arguments)}")
            arg_values = [self.evaluate(arg) for arg in expr.arguments]
            func_env = Environment(parent=self.env)
            for param, arg_value in zip(parameters, arg_values):
                func_env.set(param, arg_value)
            original_env = self.env
            self.env = func_env
            try:
                for stmt in body:
                    self.interpret(stmt)
            except ReturnException as e:
                return e.value
            finally:
                self.env = original_env
            return None 

        else:
            raise Exception(f"Unsupported expression: {type(expr).__name__}")

    def _apply_operator(self, operator, left, right):
        if operator == "SUM OF":
            return left + right
        elif operator == "DIFF OF":
            return left - right
        elif operator == "PRODUKT OF":
            return left * right
        elif operator == "QUOSHUNT OF":
            return left / right
        elif operator == "MOD OF":
            return left % right
        elif operator == "BIGGR OF":
            return max(left, right)
        elif operator == "SMALLR OF":
            return min(left, right)
        elif operator == "BOTH OF":
            return bool(left) and bool(right)
        elif operator == "EITHER OF":
            return bool(left) or bool(right)
        elif operator == "WON OF":
            return bool(left) != bool(right)
        else:
            raise Exception(f"Unknown operator: {operator}")
        