import clouscript


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
    ]
)

# 2. Write a piece of code to be lexed
string = """
1 2 "3" "hello world!" 4 5
"""

# 3. Lex it!
elements = lexer.lex(string)

# 4. Print the elements
for element in elements:
    print(element)