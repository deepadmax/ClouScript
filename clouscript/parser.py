from .elements import Sequence

from .exceptions import MismatchedParentheses


class Parser:
    def __init__(self, parenthesis=None, delimiter=None):
        self.parenthesis = parenthesis
        self.delimiter = delimiter

    def parse(self, elements):
        """Parse an array of elements
        and generate an abstract syntax tree
        """

        # Initialize stack to deal with navigating
        # up and down parenthesized sections
        stack = [[]]
        
        # History of opened parenthese
        history = [None]


        i = 0
        while i < len(elements):
            e = elements[i]
            
            if issubclass(type(e), self.parenthesis):
                # Open up a new section
                # when a left-hand parenthesis is found
                if e.handedness == self.parenthesis.LEFT:
                    stack[-1].append([])
                    stack.append(stack[-1][-1])
                    history.append(type(e))

                # Close down the last opened section
                # when a right-hand parenthesis is found
                elif e.handedness == self.parenthesis.RIGHT:
                    # If the closing parenthesis does not match
                    # the type that was most recently opened,
                    # there has been a mismatch
                    if type(e) is not history[-1]:
                        raise MismatchedParentheses(
                                f'{type(e)} does not match with {history[-1]}')

                    # Move back up the tree
                    stack.pop()
                    history.pop()

                    # Tidy up section by delimiting,
                    # forming functions and infixes, etc.
                    section = stack[-1][-1]
                    section = self.tidy_up(section)
                    
                    # Insert section into a Sequence element of the Parenthesis
                    stack[-1][-1] = e.sequence(section)

            else:
                # If the element is not a parenthesis,
                # add it to the currently opened section
                stack[-1].append(e)

            i += 1

        # Tidy up top layer and put everything
        # into an overarching root element
        return Root(self.tidy_up(stack[-1]))

    def tidy_up(self, section):
        """Tidy up an array by delimiting,
        forming functions and infixes, etc.
        """

        if self.delimiter is not None:
            section = self.delimiter.delimit(section)

        # TODO: Add function formation

        # TODO: Add infixing

        return section


class Root(Sequence):
    """The root of the abstract syntax tree"""