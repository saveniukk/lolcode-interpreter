"""
LOLCODE Interpreter - Executes AST nodes in an environment
Handles variable scoping, function calls, and control structures.
"""

from src.ast_nodes import *


class Environment:
    """Manages variable and function scoping with parent references."""
    
    def __init__(self, parent: 'Environment' = None):
        self.variables = {}
        self.functions = {}
        self.parent = parent

    def set(self, name: str, value) -> None:
        """Assign a value to a variable in current scope."""
        self.variables[name] = value

    def get(self, name: str):
        """Retrieve variable value from current or parent scope."""
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"Undefined variable: '{name}'")

    def define_function(self, name: str, parameters: list, body: list) -> None:
        """Define a function in current scope."""
        self.functions[name] = (parameters, body)

    def get_function(self, name: str) -> tuple:
        """Retrieve function definition from current or parent scope."""
        if name in self.functions:
            return self.functions[name]
        if self.parent:
            return self.parent.get_function(name)
        raise NameError(f"Undefined function: '{name}'")


class ReturnException(Exception):
    """Special exception to handle function return values."""
    def __init__(self, value):
        self.value = value


class Interpreter:
    """Evaluates AST nodes and executes program logic."""
    
    def __init__(self):
        self.env = Environment()
        # Operator to function mapping
        self.OPERATORS = {
            "SUM OF": lambda a, b: a + b,
            "DIFF OF": lambda a, b: a - b,
            "PRODUKT OF": lambda a, b: a * b,
            "QUOSHUNT OF": lambda a, b: a / b,
            "MOD OF": lambda a, b: a % b,
            "BIGGR OF": max,
            "SMALLR OF": min,
            "BOTH OF": lambda a, b: bool(a) and bool(b),
            "EITHER OF": lambda a, b: bool(a) or bool(b),
            "WON OF": lambda a, b: bool(a) != bool(b)
        }

    def interpret(self, node) -> None:
        """Execute AST node based on its type."""
        if isinstance(node, Program):
            self._execute_statements(node.statements)
        
        elif isinstance(node, VisibleStatement):
            print(self.evaluate(node.expression))
        
        elif isinstance(node, Assignment):
            self.env.set(node.variable_name, self.evaluate(node.value_expr))
        
        elif isinstance(node, IfStatement):
            self._handle_if_statement(node)
        
        elif isinstance(node, Loop):
            self._handle_loop(node)
        
        elif isinstance(node, FunctionDefinition):
            self.env.define_function(node.name, node.parameters, node.body)
        
        elif isinstance(node, ReturnStatement):
            raise ReturnException(self.evaluate(node.expression))
        
        elif not isinstance(node, NoOp):
            raise RuntimeError(f"Unsupported node: {type(node).__name__}")

    def evaluate(self, expr):
        """Evaluate expression node and return its value."""
        if isinstance(expr, Literal):
            return expr.value
        
        if isinstance(expr, Variable):
            return self.env.get(expr.name)
        
        if isinstance(expr, BinaryOperation):
            return self._evaluate_binary_operation(expr)
        
        if isinstance(expr, FunctionCall):
            return self._call_function(expr)
        
        raise RuntimeError(f"Unsupported expression: {type(expr).__name__}")

    def _execute_statements(self, statements: list) -> None:
        """Execute a sequence of statements."""
        for stmt in statements:
            self.interpret(stmt)

    def _handle_if_statement(self, node: IfStatement) -> None:
        """Execute conditional branching logic."""
        condition = self.evaluate(node.condition)
        block = node.true_block if condition else node.false_block
        if block:
            self._execute_statements(block)

    def _handle_loop(self, node: Loop) -> None:
        """Execute loop iteration logic."""
        start_val = self.evaluate(node.start_expr)
        end_val = self.evaluate(node.end_expr)
        
        if not isinstance(start_val, int) or not isinstance(end_val, int):
            raise RuntimeError("Loop bounds must be integers")
        
        for i in range(start_val, end_val + 1):
            self.env.set(node.variable_name, i)
            self._execute_statements(node.body)

    def _evaluate_binary_operation(self, expr: BinaryOperation):
        """Evaluate binary operator expressions."""
        left_val = self.evaluate(expr.left)
        right_val = self.evaluate(expr.right)
        
        if expr.operator in self.OPERATORS:
            return self.OPERATORS[expr.operator](left_val, right_val)
        raise RuntimeError(f"Unknown operator: '{expr.operator}'")

    def _call_function(self, expr: FunctionCall):
        """Execute function call with new environment scope."""
        params, body = self.env.get_function(expr.name)
        
        if len(params) != len(expr.arguments):
            raise RuntimeError(
                f"Function '{expr.name}' expects {len(params)} arguments, "
                f"got {len(expr.arguments)}"
            )
        
        # Create function execution environment
        func_env = Environment(parent=self.env)
        arg_values = [self.evaluate(arg) for arg in expr.arguments]
        for param, arg_val in zip(params, arg_values):
            func_env.set(param, arg_val)
        
        # Execute function body
        original_env = self.env
        self.env = func_env
        try:
            self._execute_statements(body)
            return None  # No return statement encountered
        except ReturnException as e:
            return e.value
        finally:
            self.env = original_env