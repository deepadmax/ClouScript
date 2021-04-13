

class ClouScriptException(Exception):
    """Problem related to ClouScript"""



# ┌────────┐
# │ LEXING │
# └────────┘

class LexingError(ClouScriptException):
    """String is not compliant with lexing rules"""

class NoMatch(LexingError):
    """No lexing rule could be matched"""


# [ DELIMITER ]

class DelimiterError(LexingError):
    """Problem with delimiting elements"""

class InvalidDelimiter(DelimiterError):
    """Element type is a valid parenthesis group
    but the value is not a valid parenthesis"""



# ┌─────────┐
# │ PARSING │
# └─────────┘

class ParsingError(ClouScriptException):
    """Elements are not compliant with parsing rules"""


# [ PARENTHESIS ]

class ParenthesisError(ParsingError):
    """Attempting to close a section
    with an incorrect right-hand parenthesis"""

class InvalidParenthesis(ParenthesisError):
    """Attempting to create an instance of
    a non-existant Parenthesis subclass"""

class MismatchedParentheses(ParenthesisError):
    """Attempting to close a section
    with an incorrect right-hand parenthesis"""

class UndefinedSequence(ParenthesisError):
    """Sequence class has not been defined for Parenthesis"""