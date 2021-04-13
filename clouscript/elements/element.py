

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