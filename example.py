import clouscript



# ┌─────────────┐
# │ PARENTHESES │
# └─────────────┘

from clouscript.elements.sequence import Sequence
from clouscript.elements.parenthesis import Parenthesis


class Square(Parenthesis):
    left = '['
    right = ']'
    
    class List(Sequence): pass

class Round(Parenthesis):
    left = '('
    right = ')'
    
    class Arguments(Sequence): pass



# ┌────────────┐
# │ DELIMITERS │
# └────────────┘

from clouscript.elements.delimiter import Delimiter


Delimiter.FLATTEN_MODE = 'local'


class Semicolon(Delimiter):
    character = ';'

class Comma(Delimiter):
    character = ','


Delimiter.set_order([
    Semicolon,
    Comma
])



# ┌───────┐
# │ LEXER │
# └───────┘

from clouscript.lexer import Lexer
from clouscript.elements.basics import Integer, String


# 1. Define a lexer
lexer = Lexer(
    [
        Integer,
        String
    ],
    [
        Parenthesis,
        Delimiter
    ]
)

# 2. Write a piece of code to be lexed
string = """
1 2; [3, 4]
"""

# 3. Lex string
elements = list(lexer.lex(string))



# ┌────────┐
# │ PARSER │
# └────────┘

from clouscript.parser import Parser


# 1. Define a parser
parser = Parser(
    parenthesis=Parenthesis
)

# 2. Parse elements and print AST
root = parser.parse(elements)
print(root)