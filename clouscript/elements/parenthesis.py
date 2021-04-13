import re

from .element import Element
from .sequence import Sequence

from ..exceptions import InvalidParenthesis, UndefinedSequence


class Parenthesis(Element):
    """Inherit from this to define a parenthesis type
    
    Ex.
    class Bracket(Parenthesis):
        left = '['
        right = ']'
        
        class List(Sequence): pass
        
    Each Parenthesis subclass must have its own Sequence class
    """
    
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'

    @classmethod
    @property
    def regex(cls):
        """Generate a regular expression for all subclass parentheses"""

        # Regular expression for every subclass parenthesis pair
        res = [f'{p.left}{p.right}' for p in cls.__subclasses__()]
        
        # Overwrite function to stored generated regex
        cls.regex = f'[{re.escape("".join(res))}]'

        return cls.regex

    @classmethod
    def create(cls, groups):
        """Create a subclass Parenthesis from match groups"""
        
        for parenthesis in cls.__subclasses__():
            if groups[0] == parenthesis.left:
                return parenthesis(cls.LEFT)

            if groups[0] == parenthesis.right:
                return parenthesis(cls.RIGHT)

        raise InvalidParenthesis(
                f'{repr(groups[0])} is not a valid parenthesis')

    def __init__(self, handedness):
        # Handedness: (Parenthesis.Left | Parenthesis.Right)
        self.handedness = handedness

    def __repr__(self):
        if self.handedness == self.LEFT:
            return f'{self.left}{type(self).__name__}{self.left}'
        if self.handedness == self.RIGHT:
            return f'{self.right}{type(self).__name__}{self.right}'
        
        raise ValueError(
                f'Handedness must be either {self.LEFT} or {self.RIGHT}')

    @classmethod
    @property
    def sequence(cls):
        """Find and access the Sequence of this Parenthesis"""
        
        # Iterate over all attributes
        for attribute in dir(cls):
            attr = getattr(cls, attribute)
            
            # When a Sequence is found,
            # use that to replace this method and stop searching
            if isinstance(attr, type) and issubclass(attr, Sequence):
                cls.sequence = attr
                break
        else:
            raise UndefinedSequence(
                    f'Sequence is not defined for {cls.__name__}')

        return cls.sequence