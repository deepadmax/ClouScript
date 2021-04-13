import re

from .exceptions import NoMatch


class Lexer:
    def __init__(self, alpha, beta):
        """Do make sure to provide the Element subclasses in an order
        that will make sure they can all be matched.
        For example, you would not want an integer before a float,
        because then it would match a float as an integer.

        Arguments:
            alpha -- list: Element subclasses which require spacing inbetween
                            themselves and other surrounding alpha elements
            beta -- list: Element subclasses which may be found
                            immediately beside another element
        """

        self.alpha = alpha
        self.beta = beta

    def lex(self, string):
        """Segment a string into Elements"""

        # Since alpha elements may not be found immediately
        # beside another alpha element, keep track of whether
        # the latest match was one
        allow_alpha = True
        

        # Read the entire string, left to right,
        # matching patterns for element types
        # and yield an Element when found

        i = 0
        while i < len(string):
            # Because it is not possible to continue a while-loop
            # from within a for-loop, we are noting down when a match
            # has been made and continuing afterward if one has
            matched = False


            # 1. Loop over and match with betas
            
            for element_type in self.beta:
                if m := re.match(element_type.regex, string[i:]):
                    # If the element subclass is not to be ignored,
                    # yield an Element from it using the matched string
                    if not element_type.ignore:
                        yield element_type.create([m.group(0), *m.groups()])

                    # Allow alpha elements to be matched after a beta
                    allow_alpha = True

                    # Move the cursor along
                    i += len(m.group(0))
                    
                    # Mark as matched
                    # and stop matching any more
                    matched = True
                    break

            # Continue to next iteration
            # if a beta element has already been found
            if matched:
                continue


            # 2. If alpha elements are allowed,
            # loop over and match with alphas
            
            if allow_alpha:
                for element_type in self.alpha:
                    if m := re.match(element_type.regex, string[i:]):
                        # If the element subclass is not to be ignored,
                        # yield an Element from it using the matched string
                        if not element_type.ignore:
                            yield element_type.create([m.group(0), *m.groups()])

                        # Disallow alpha elements to precede this one
                        allow_alpha = False

                        # Move the cursor along
                        i += len(m.group(0))
                        
                        # Mark as matched
                        # and stop matching any more
                        matched = True
                        break
                
                # else:
                #     # If neither a beta nor an alpha element has been found
                #     # and there has already been spacing, the syntax is incorrect
                #     raise NoMatch(f'No element could be found at {i}')

            # Continue to next iteration
            # if an alpha element has already been found
            if matched:
                continue


            # 3. Otherwise, any spacing must be found

            if m := re.match(r'[\s\n]+', string[i:]):
                # Allow alpha elements to be matched after a beta
                allow_alpha = True

                # Move the cursor along
                i += len(m.group(0))

                continue
            
            
            # (4. Failure.)
            raise NoMatch(f'No element could be found at {i}')