

class ClouScriptException(Exception):
    """Problem related to ClouScript"""


# ┌────────┐
# │ LEXING │
# └────────┘

class LexingError(ClouScriptException):
    """String is not compliant with lexing rules"""

class NoMatch(LexingError):
    """No lexing rule could be matched"""