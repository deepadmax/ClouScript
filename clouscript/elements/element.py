

class Element:
    """The most basic element in the code.
    It can represent anything from a function call
    to an integer or a collection.
    
    All types of Elements should inherit from this class
    This class should never be used directly.
    """

    regex = r'.'
    ignore = False

    @classmethod
    def create(cls, groups):
        """Create an Element of this type.
        Always use this function instead of the default initialisation.
        """
        return cls(groups)

    def __init__(self, groups):
        """The initialization of any Element is always given
        a list of regular expression match groups from which
        to extract needed values
        """
    
    def __repr__(self):
        return f'<{type(self).__name__}>'

    def __str__(self):
        return self.pretty()

    def pretty(self, indent=0):
        """Display the entire hierarchy
        of subordinate elements as a tree structure
        """
        return repr(self)
        
    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)

    def call(self, *args, **kwargs):
        """Calculate the value of the Element"""
        return None