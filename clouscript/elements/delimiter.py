import re

from .element import Element
from .sequence import Sequence

from ..exceptions import InvalidDelimiter


class Delimiter(Element):
    """Inherit from this to define a delimiter type
    
    Ex.
    class Comma(Delimiter):
        character = ','

    Delimiter.set_order must be called to define the order or priority
    """

    ALLOW_EMPTY_SECTIONS = False
    FLATTEN_MODE = 'global'

    @classmethod
    def set_order(cls, delimiters):
        """Set the order of delimiting for delimiter subclasses"""
        cls.ORDER = delimiters

    @classmethod
    @property
    def regex(cls):
        """Generate a regular expression for all subclass delimiters"""

        # Regex for every subclass delimiter
        regex = f'[{"".join([p.character for p in cls.__subclasses__()])}]'
        
        # Overwrite function to stored generated regex
        cls.regex = regex

        return cls.regex

    @classmethod
    def create(cls, groups):
        """Create a subclass Parenthesis from match groups"""
        
        for delimiter in cls.__subclasses__():
            if groups[0] == delimiter.character:
                return delimiter(groups)

        raise InvalidDelimiter(
                f'{repr(groups[0])} is not a valid delimiter')