from hs.lib.staticproperty import staticproperty
from hs.lib.Symbols.Tokens import Token

class Variable(Token):
    def __init__(self, name: str = None):
        super().__init__()
        self.name: str = name

    @staticproperty
    def string_identifier(self) -> str:
        return "variable"

    def __str__(self) -> str:
        return self.name

    @staticproperty
    def regex() -> str:
        return r"^([a-zA-Z_]+)([a-zA-Z_0-9]*)$"