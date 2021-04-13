from .element import Element


class Fundamental(Element):
    """One-value Elements inherit from this"""

    def __init__(self, groups):
        self.value = groups[0]
    
    def __repr__(self):
        return f'<{type(self).__name__}: {self.value}>'

    def call(self):
        return self.value


class Integer(Fundamental):
    regex = r'(\-?)(?:0x([0-9a-fA-F]+)|(\d+))'
    
    def __init__(self, groups):
        # It is a hexadecimal if the group 2 is matched
        if groups[2]:
            self.value = int(groups[2], 16)

        # It is an integer if the group 3 is matched
        if groups[3]:
            self.value = int(groups[3])

        # It is a negative integer if the group 1 is matched
        if groups[1]:
            self.value = -self.value


class String(Fundamental):
    regex = r'\"((?:\\"|.|\n)*?)\"'
    
    def __init__(self, groups):
        self.value = groups[1]