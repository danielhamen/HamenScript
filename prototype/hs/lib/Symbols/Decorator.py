import re

from hs.lib.Symbols.Variable import Variable
from hs.lib.staticproperty import staticproperty
from hs.lib.Symbols.Tokens import Token

class Decorator(Token):
    def __init__(self, fn: str = None):
        super().__init__()
        self.fn: str = fn
        if fn.startswith("@"):
            self.fn: str = fn[1:]

    @staticproperty
    def string_identifier(self) -> str:
        return "decorator"
    
    @staticmethod
    def test(value: str) -> bool:
        return True if re.findall(Decorator.regex, value) else False

    @staticproperty
    def regex(self) -> str:
        return r"^@([a-zA-Z_]+[a-zA-Z_0-9]*)$"

    def __str__(self) -> str:
        return self.fn