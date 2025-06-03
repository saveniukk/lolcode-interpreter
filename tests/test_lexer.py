import pytest
from src.lexer import Lexer

@pytest.mark.parametrize("source, expected_type, expected_value", [
    ("HAI", "HAI", "HAI"),
    ("KTHXBYE", "KTHXBYE", "KTHXBYE"),
    ("VISIBLE", "VISIBLE", "VISIBLE"),
    ("I HAS A", "I_HAS_A", "I HAS A"),
    ("ITZ", "ITZ", "ITZ"),
    ("R", "R", "R"),
    ("SUM OF", "SUM_OF", "SUM OF"),
    ("DIFF OF", "DIFF_OF", "DIFF OF"),
    ("PRODUKT OF", "PRODUKT_OF", "PRODUKT OF"),
    ("QUOSHUNT OF", "QUOSHUNT_OF", "QUOSHUNT OF"),
    ("MOD OF", "MOD_OF", "MOD OF"),
    ("BIGGR OF", "BIGGR_OF", "BIGGR OF"),
    ("SMALLR OF", "SMALLR_OF", "SMALLR OF"),
    ("BOTH OF", "BOTH_OF", "BOTH OF"),
    ("EITHER OF", "EITHER_OF", "EITHER OF"),
    ("WON OF", "WON_OF", "WON OF"),
    ("AN", "AN", "AN"),
    ("O RLY?", "IF", "O RLY?"),
    ("YA RLY", "YA_RLY", "YA RLY"),
    ("NO WAI", "NO_WAI", "NO WAI"),
    ("OIC", "OIC", "OIC"),
])

def test_keywords(source, expected_type, expected_value):
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    assert len(tokens) == 1
    assert tokens[0].type == expected_type
    assert tokens[0].value == expected_value
    assert tokens[0].line == 1

@pytest.mark.parametrize("source, expected_value", [
    ("var", "var"),
    ("_var", "_var"),
    ("var1", "var1"),
])

def test_identifiers(source, expected_value):
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    assert len(tokens) == 1
    assert tokens[0].type == "IDENTIFIER"
    assert tokens[0].value == expected_value
    assert tokens[0].line == 1

@pytest.mark.parametrize("source, expected_value", [
    ("123", "123"),
    ("-5", "-5"),
    ("0", "0"),
])

def test_numbers(source, expected_value):
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    assert len(tokens) == 1
    assert tokens[0].type == "NUMBR"
    assert tokens[0].value == expected_value
    assert tokens[0].line == 1

@pytest.mark.parametrize("source, expected_value", [
    ('"hello"', '"hello"'),
    ('"hello world"', '"hello world"'),
    ('""', '""'),
])

def test_strings(source, expected_value):
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    assert len(tokens) == 1
    assert tokens[0].type == "STRING"
    assert tokens[0].value == expected_value
    assert tokens[0].line == 1

def test_simple_program():
    source_code = "HAI\nI HAS A var ITZ 5\nVISIBLE var\nKTHXBYE"
    expected = [
        ("HAI", "HAI", 1),
        ("I_HAS_A", "I HAS A", 2),
        ("IDENTIFIER", "var", 2),
        ("ITZ", "ITZ", 2),
        ("NUMBR", "5", 2),
        ("VISIBLE", "VISIBLE", 3),
        ("IDENTIFIER", "var", 3),
        ("KTHXBYE", "KTHXBYE", 4),
    ]

    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    assert len(tokens) == len(expected)

    for token, (exp_type, exp_value, exp_line) in zip(tokens, expected):
        assert token.type == exp_type
        assert token.value == exp_value
        assert token.line == exp_line

def test_skip_spaces_and_comments():
    source_code = "HAI   \t  KTHXBYE"
    expected = [
        ("HAI", "HAI", 1),
        ("KTHXBYE", "KTHXBYE", 1),
    ]

    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    assert len(tokens) == len(expected)

    for token, (exp_type, exp_value, exp_line) in zip(tokens, expected):
        assert token.type == exp_type
        assert token.value == exp_value
        assert token.line == exp_line

    source_code = "HAI BTW this is a comment\nKTHXBYE"
    expected = [
        ("HAI", "HAI", 1),
        ("KTHXBYE", "KTHXBYE", 2),
    ]

    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    assert len(tokens) == len(expected)

    for token, (exp_type, exp_value, exp_line) in zip(tokens, expected):
        assert token.type == exp_type
        assert token.value == exp_value
        assert token.line == exp_line

def test_illegal_character():
    source_code = "HAI @"
    lexer = Lexer(source_code)
    with pytest.raises(SyntaxError, match="Illegal character at line 1: @"):
        lexer.tokenize()

def test_empty_source():
    lexer = Lexer("")
    tokens = lexer.tokenize()
    assert tokens == []

def test_only_spaces_and_comments():
    source_code = "   \n   \n"
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    assert tokens == []

    source_code = "BTW comment\n"
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    assert tokens == []
