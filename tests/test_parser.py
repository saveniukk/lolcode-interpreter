import pytest
from src.parser import Parser
from src.ast_nodes import *
from src.lexer import Token

def create_tokens(token_list):
    return [Token(type_, value, 1) for type_, value in token_list]

def test_basic_program():
    tokens = create_tokens([("HAI", "HAI"), ("KTHXBYE", "KTHXBYE")])
    parser = Parser(tokens)
    ast = parser.parse()

    expected = Program([])

    assert ast == expected

def test_missing_hai():
    tokens = create_tokens([("KTHXBYE", "KTHXBYE")])
    parser = Parser(tokens)

    with pytest.raises(SyntaxError, match="Expected HAI"):
        parser.parse()

def test_missing_kthxbye():
    tokens = create_tokens([("HAI", "HAI")])
    parser = Parser(tokens)

    with pytest.raises(SyntaxError, match="Expected KTHXBYE"):
        parser.parse()

def test_variable_declaration():
    tokens = create_tokens([
        ("HAI", "HAI"),
        ("I_HAS_A", "I HAS A"),
        ("IDENTIFIER", "VAR"),
        ("KTHXBYE", "KTHXBYE")
    ])
    parser = Parser(tokens)
    ast = parser.parse()

    expected = Program([Assignment("VAR", Literal(None))])

    assert ast == expected

def test_variable_declaration_with_init():
    tokens = create_tokens([
        ("HAI", "HAI"),
        ("I_HAS_A", "I HAS A"),
        ("IDENTIFIER", "VAR"),
        ("ITZ", "ITZ"),
        ("NUMBR", "5"),
        ("KTHXBYE", "KTHXBYE")
    ])
    parser = Parser(tokens)
    ast = parser.parse()

    expected = Program([Assignment("VAR", Literal(5))])

    assert ast == expected

def test_assignment():
    tokens = create_tokens([
        ("HAI", "HAI"),
        ("IDENTIFIER", "VAR"),
        ("R", "R"),
        ("NUMBR", "10"),
        ("KTHXBYE", "KTHXBYE")
    ])
    parser = Parser(tokens)
    ast = parser.parse()

    expected = Program([Assignment("VAR", Literal(10))])

    assert ast == expected

def test_visible_literal():
    tokens = create_tokens([
        ("HAI", "HAI"),
        ("VISIBLE", "VISIBLE"),
        ("STRING", '"Hello"'),
        ("KTHXBYE", "KTHXBYE")
    ])
    parser = Parser(tokens)
    ast = parser.parse()

    expected = Program([VisibleStatement(Literal("Hello"))])

    assert ast == expected

def test_visible_variable():
    tokens = create_tokens([
        ("HAI", "HAI"),
        ("VISIBLE", "VISIBLE"),
        ("IDENTIFIER", "VAR"),
        ("KTHXBYE", "KTHXBYE")
    ])
    parser = Parser(tokens)
    ast = parser.parse()

    expected = Program([VisibleStatement(Variable("VAR"))])

    assert ast == expected

def test_binary_operation():
    tokens = create_tokens([
        ("HAI", "HAI"),
        ("VISIBLE", "VISIBLE"),
        ("SUM_OF", "SUM OF"),
        ("NUMBR", "3"),
        ("AN", "AN"),
        ("NUMBR", "4"),
        ("KTHXBYE", "KTHXBYE")
    ])
    parser = Parser(tokens)
    ast = parser.parse()

    expected = Program([VisibleStatement(BinaryOperation("SUM OF", Literal(3), Literal(4)))])

    assert ast == expected

def test_nested_expression():
    tokens = create_tokens([
        ("HAI", "HAI"),
        ("VISIBLE", "VISIBLE"),
        ("SUM_OF", "SUM OF"),
        ("NUMBR", "3"),
        ("AN", "AN"),
        ("PRODUKT_OF", "PRODUKT OF"),
        ("NUMBR", "2"),
        ("AN", "AN"),
        ("NUMBR", "2"),
        ("KTHXBYE", "KTHXBYE")
    ])
    parser = Parser(tokens)
    ast = parser.parse()

    expected = Program([
        VisibleStatement(
            BinaryOperation("SUM OF",
                Literal(3),
                BinaryOperation("PRODUKT OF", Literal(2), Literal(2))
            )
        )
    ])

    assert ast == expected

def test_if_statement_true_block():
    tokens = create_tokens([
        ("HAI", "HAI"),
        ("IF", "IF"),
        ("YA_RLY", "YA RLY"),
        ("VISIBLE", "VISIBLE"),
        ("STRING", '"True"'),
        ("OIC", "OIC"),
        ("KTHXBYE", "KTHXBYE")
    ])
    parser = Parser(tokens)
    ast = parser.parse()

    expected = Program([
        IfStatement(
            Variable("IT"),
            [VisibleStatement(Literal("True"))],
            None
        )
    ])

    assert ast == expected

def test_if_statement_true_false_blocks():
    tokens = create_tokens([
        ("HAI", "HAI"),
        ("IF", "IF"),
        ("YA_RLY", "YA RLY"),
        ("VISIBLE", "VISIBLE"),
        ("STRING", '"True"'),
        ("NO_WAI", "NO WAI"),
        ("VISIBLE", "VISIBLE"),
        ("STRING", '"False"'),
        ("OIC", "OIC"),
        ("KTHXBYE", "KTHXBYE")
    ])
    parser = Parser(tokens)
    ast = parser.parse()

    expected = Program([
        IfStatement(
            Variable("IT"),
            [VisibleStatement(Literal("True"))],
            [VisibleStatement(Literal("False"))]
        )
    ])

    assert ast == expected

def test_missing_an_in_binary_op():
    tokens = create_tokens([
        ("HAI", "HAI"),
        ("VISIBLE", "VISIBLE"),
        ("SUM_OF", "SUM OF"),
        ("NUMBR", "3"),
        ("NUMBR", "4"),
        ("KTHXBYE", "KTHXBYE")
    ])
    parser = Parser(tokens)

    with pytest.raises(SyntaxError, match="Expected AN"):
        parser.parse()

def test_unexpected_token():
    tokens = create_tokens([
        ("HAI", "HAI"),
        ("VISIBLE", "VISIBLE"),
        ("UNKNOWN", "UNKNOWN"),
        ("KTHXBYE", "KTHXBYE")
    ])
    parser = Parser(tokens)

    with pytest.raises(SyntaxError, match="Unexpected token UNKNOWN"):
        parser.parse()

def test_missing_oic_in_if():
    tokens = create_tokens([
        ("HAI", "HAI"),
        ("IF", "IF"),
        ("YA_RLY", "YA RLY"),
        ("VISIBLE", "VISIBLE"),
        ("STRING", '"True"'),
        ("KTHXBYE", "KTHXBYE") 
    ])
    parser = Parser(tokens)

    with pytest.raises(SyntaxError, match="Expected OIC"):
        parser.parse()
