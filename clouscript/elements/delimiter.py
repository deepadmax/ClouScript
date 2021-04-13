import re

from .element import Element
from .sequence import Sequence

from ..exceptions import InvalidDelimiter, EmptySection


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

    @classmethod
    def contains(cls, elements):
        """Check if there are any delimiter elements"""
        
        if not any(type(e) is cls for e in elements):
            return elements

    @classmethod
    def delimit_single(cls, elements):
        """Delimit an array of elements by this delimiter"""

        sections = [[]]


        if cls.contains(elements):
            return elements


        # Separate the elements between delimiters
        # by starting a new list whenever this delimiter is encountered
        for element in elements:
            if type(element) is cls:
                sections.append([])
            else:
                sections[-1].append(element)

        
        # Raise error if there are empty sections and it is not allowed
        if not cls.ALLOW_EMPTY_SECTIONS:
            if not all(sections):
                raise EmptySection('Empty sections are not allowed')


        if cls.FLATTEN_MODE == 'global' and len(max(sections, key=len)) <= 1:
            # Flatten all sections if there are no sections longer than one element
            for i, section in enumerate(sections):
                if len(section) > 0:
                    sections[i] = section[0]

        if cls.FLATTEN_MODE == 'local':
            # Flatten sections which contain only one element
            for i, section in enumerate(sections):
                if len(section) == 1:
                    sections[i] = section[0]


        # Convert all lists into sequence elements
        for i, section in enumerate(sections):
            if type(section) is list:
                sections[i] = Sequence(section)

        return sections

    @classmethod
    def delimit_multiple(cls, elements, delimiters):
        """Delimit an array of elements by multiple delimiters"""

        if len(delimiters) == 0:
            return elements

        
        # Segment array by priority
        
        for delimiter in delimiters:
            elements = delimiter.delimit_single(elements)
            
            # Do not attempt to segment any deeper
            # if there are no more delimiters left
            # or if the array is not long enough
            if len(delimiters) - 1 < 1 or len(elements) <= 1:
                continue

            # For every element in the newly segmented array,
            # if one is a sequence, segment its parts
            for i, element in enumerate(elements):
                if type(element) is Sequence:
                    elements[i] = Sequence(cls.delimit_multiple(
                                    element.array, delimiters[1:]))

        return elements

    @classmethod
    def delimit(cls, elements):
        """Delimit an array of elements by delimiters"""
        return cls.delimit_multiple(elements, cls.ORDER)