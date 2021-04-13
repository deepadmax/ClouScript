from .element import Element


class Sequence(Element):
    """Base object for storing a sequence of Elements"""
    
    def __init__(self, array):
        self.array = array

    def pretty(self, indent=0):
        indent += 1
        
        string = f'<{type(self).__name__}>\n'
        string += '\n'.join('  ' * indent + element.pretty(indent)
                                        for element in self.array)
        return string