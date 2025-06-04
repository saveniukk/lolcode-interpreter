import re

TOKEN_TYPES = [
    ('HAI', r'HAI'),
    ('KTHXBYE', r'KTHXBYE'),
    ('VISIBLE', r'VISIBLE'),
    ('I_HAS_A', r'I HAS A'),
    ('ITZ', r'ITZ'),
    ('R', r'R'),
    ('SUM_OF', r'SUM OF'),
    ('DIFF_OF', r'DIFF OF'),
    ('PRODUKT_OF', r'PRODUKT OF'),
    ('QUOSHUNT_OF', r'QUOSHUNT OF'),
    ('MOD_OF', r'MOD OF'),
    ('BIGGR_OF', r'BIGGR OF'),
    ('SMALLR_OF', r'SMALLR OF'),
    ('BOTH_OF', r'BOTH OF'),
    ('EITHER_OF', r'EITHER OF'),
    ('WON_OF', r'WON OF'),
    ('AN', r'AN'),
    ('IF', r'O RLY\?'),
    ('YA_RLY', r'YA RLY'),
    ('NO_WAI', r'NO WAI'),
    ('OIC', r'OIC'),
    ('HOW_IZ_I', r'HOW IZ I'),
    ('IF_U_SAY_SO', r'IF U SAY SO'),
    ('FOUND_YR', r'FOUND YR'),
    ('IM_IN_YR', r'IM IN YR'),
    ('IM_OUTTA_YR', r'IM OUTTA YR'),
    ('YR', r'YR'),
    ('UPPIN', r'UPPIN'),
    ('NERFIN', r'NERFIN'),
    ('TIL', r'TIL'),
    ('WILE', r'WILE'),
    ('NUMBR', r'-?\d+'),
    ('STRING', r'"[^"]*"'),
    ('COMMENT', r'BTW[^\n]*'), 
    ('BIGGR', r'BIGGR'),
    ('THAN', r'THAN'),
    ('IDENTIFIER', r'[A-Za-z_][A-Za-z0-9_]*'),
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),
]

COMPILED_TOKEN_TYPES = [(name, re.compile(pattern)) for name, pattern in TOKEN_TYPES]


class Token:
    def __init__(self, type_, value, line):
        self.type = type_
        self.value = value
        self.line = line

    def __repr__(self):
        return f'Token({self.type}, {repr(self.value)}, line={self.line})'


class Lexer:
    def __init__(self, source_code):
        self.source = source_code
        self.tokens = []
        self.line = 1

    def tokenize(self):
        pos = 0
        while pos < len(self.source):
            match = None
            for token_type, regex in COMPILED_TOKEN_TYPES:
                match = regex.match(self.source, pos)
                if match:
                    value = match.group(0)
                    if token_type == 'NEWLINE':
                        self.line += 1
                    elif token_type == 'SKIP' or token_type == 'COMMENT':
                        pass
                    else:
                        token = Token(token_type, value, self.line)
                        self.tokens.append(token)
                    pos = match.end()
                    break
            if not match:
                raise SyntaxError(f'Illegal character at line {self.line}: {self.source[pos]}')
        return self.tokens
    