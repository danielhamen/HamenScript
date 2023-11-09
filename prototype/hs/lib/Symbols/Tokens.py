from hs.lib.staticproperty import staticproperty

class Token:
    def __init__(self):
        """
        Represents a generic token in the source code.

        Attributes:
            token_name (str): The type name of the token.
        """
        self.token_name: str

    def __str__(self) -> str:
        try:
            return self.toString()
        except:
            return ""