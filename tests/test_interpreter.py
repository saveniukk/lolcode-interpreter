import pytest
from unittest.mock import patch, call
from src.ast_nodes import *
from src.interpreter import Interpreter


@patch('builtins.print')
def test_assignment_and_visible(mocked_print):
    interp = Interpreter()
    prog = Program([
        Assignment("x", Literal(5)),
        VisibleStatement(Variable("x"))
    ])
    interp.interpret(prog)
    mocked_print.assert_called_with(5)


@pytest.mark.parametrize("operator, left, right, expected", [
    ("SUM OF", 3, 4, 7),
    ("DIFF OF", 10, 3, 7),
    ("PRODUKT OF", 2, 5, 10),
    ("QUOSHUNT OF", 10, 2, 5.0),
    ("MOD OF", 10, 3, 1),
])
def test_binary_arithmetic_operations(operator, left, right, expected):
    interp = Interpreter()
    expr = BinaryOperation(operator, Literal(left), Literal(right))
    result = interp.evaluate(expr)
    assert result == expected


@pytest.mark.parametrize("operator, left, right, expected", [
    ("BIGGR OF", 3, 4, 4),
    ("BIGGR OF", 5, 2, 5),
    ("SMALLR OF", 3, 4, 3),
    ("SMALLR OF", 5, 2, 2),
])
def test_binary_comparison_operations(operator, left, right, expected):
    interp = Interpreter()
    expr = BinaryOperation(operator, Literal(left), Literal(right))
    result = interp.evaluate(expr)
    assert result == expected


@pytest.mark.parametrize("operator, left, right, expected", [
    ("BOTH OF", True, True, True),
    ("BOTH OF", True, False, False),
    ("EITHER OF", True, False, True),
    ("EITHER OF", False, False, False),
    ("WON OF", True, False, True),
    ("WON OF", True, True, False),
])
def test_binary_logical_operations(operator, left, right, expected):
    interp = Interpreter()
    expr = BinaryOperation(operator, Literal(left), Literal(right))
    result = interp.evaluate(expr)
    assert result == expected


@patch('builtins.print')
def test_if_statement_true(mocked_print):
    interp = Interpreter()
    prog = Program([
        IfStatement(Literal(True), [VisibleStatement(Literal("Yes"))], [])
    ])
    interp.interpret(prog)
    mocked_print.assert_called_with("Yes")


@patch('builtins.print')
def test_if_statement_false(mocked_print):
    interp = Interpreter()
    prog = Program([
        IfStatement(Literal(False), [], [VisibleStatement(Literal("No"))])
    ])
    interp.interpret(prog)
    mocked_print.assert_called_with("No")


@patch('builtins.print')
def test_loop(mocked_print):
    interp = Interpreter()
    prog = Program([
        Loop("i", Literal(1), Literal(3), [
            VisibleStatement(Variable("i"))
        ])
    ])
    interp.interpret(prog)
    mocked_print.assert_has_calls([call(1), call(2), call(3)])


@patch('builtins.print')
def test_expression_with_variables(mocked_print):
    interp = Interpreter()
    prog = Program([
        Assignment("x", Literal(10)),
        Assignment("y", Literal(20)),
        VisibleStatement(BinaryOperation("SUM OF", Variable("x"), Variable("y")))
    ])
    interp.interpret(prog)
    mocked_print.assert_called_with(30)


def test_undefined_variable():
    interp = Interpreter()
    prog = Program([
        VisibleStatement(Variable("z"))
    ])
    with pytest.raises(NameError):
        interp.interpret(prog)


def test_unknown_operator():
    interp = Interpreter()
    expr = BinaryOperation("UNKNOWN OP", Literal(1), Literal(2))
    with pytest.raises(Exception):
        interp.evaluate(expr)


def test_division_by_zero():
    interp = Interpreter()
    expr = BinaryOperation("QUOSHUNT OF", Literal(10), Literal(0))
    with pytest.raises(ZeroDivisionError):
        interp.evaluate(expr)


def test_invalid_operand_types():
    interp = Interpreter()
    expr = BinaryOperation("SUM OF", Literal("a"), Literal(1))
    with pytest.raises(TypeError):
        interp.evaluate(expr)


def test_nested_expressions():
    interp = Interpreter()
    expr = BinaryOperation("SUM OF", Literal(1), BinaryOperation("PRODUKT OF", Literal(2), Literal(3)))
    result = interp.evaluate(expr)
    assert result == 7


@patch('builtins.print')
def test_if_inside_loop(mocked_print):
    interp = Interpreter()
    prog = Program([
        Loop("i", Literal(1), Literal(5), [
            IfStatement(BinaryOperation("BIGGR OF", Variable("i"), Literal(3)), [
                VisibleStatement(Variable("i"))
            ], [])
        ])
    ])
    interp.interpret(prog)
    mocked_print.assert_has_calls([call(4), call(5)])


@patch('builtins.print')
def test_noop(mocked_print):
    interp = Interpreter()
    prog = Program([NoOp()])
    interp.interpret(prog)
    mocked_print.assert_not_called()


@patch('builtins.print')
def test_empty_program(mocked_print):
    interp = Interpreter()
    prog = Program([])
    interp.interpret(prog)
    mocked_print.assert_not_called()


@patch('builtins.print')
def test_reassignment(mocked_print):
    interp = Interpreter()
    prog = Program([
        Assignment("x", Literal(10)),
        VisibleStatement(Variable("x")),
        Assignment("x", Literal(20)),
        VisibleStatement(Variable("x"))
    ])
    interp.interpret(prog)
    mocked_print.assert_has_calls([call(10), call(20)])


@patch('builtins.print')
def test_variable_in_loop(mocked_print):
    interp = Interpreter()
    prog = Program([
        Assignment("sum", Literal(0)),
        Loop("i", Literal(1), Literal(5), [
            Assignment("sum", BinaryOperation("SUM OF", Variable("sum"), Variable("i")))
        ]),
        VisibleStatement(Variable("sum"))
    ])
    interp.interpret(prog)
    mocked_print.assert_called_with(15)


@patch('builtins.print')
def test_logical_expression_in_if(mocked_print):
    interp = Interpreter()
    prog = Program([
        Assignment("a", Literal(True)),
        Assignment("b", Literal(False)),
        IfStatement(BinaryOperation("BOTH OF", Variable("a"), Variable("b")), [
            VisibleStatement(Literal("Yes"))
        ], [
            VisibleStatement(Literal("No"))
        ])
    ])
    interp.interpret(prog)
    mocked_print.assert_called_with("No")


@patch('builtins.print')
def test_if_without_else(mocked_print):
    interp = Interpreter()
    prog = Program([
        IfStatement(Literal(False), [VisibleStatement(Literal("Yes"))], [])
    ])
    interp.interpret(prog)
    mocked_print.assert_not_called()
