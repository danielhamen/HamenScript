import re

from hs.lib.staticproperty import staticproperty
from hs.lib.Symbols.Tokens import Token
from hs.Globals import *

class Primitive(Token):
    def __init__(self):
        """
        Represents a primitive value token in the source code.

        Attributes:
            value (str): The string representation of the primitive value.
            prototype (dict): A dictionary of methods accessible in the language.
            constant (bool): Indicates whether the value is constant and cannot be changed.
        """
        self.value: str = ""

        self.prototype: dict = {
            "toString": lambda: self.toString()
        }

        self.is_constant = False
        self.real = None

    @staticproperty
    def string_identifier(self) -> str:
        return "primitive"

    def toString(self) -> str:
        """
        Converts the primitive value to a string representation.

        Returns:
            str: The string representation of the primitive value.
        """
        return ""

    def boolean(self) -> bool:
        """
        Returns a boolean representation of this value

        This does not only apply to booleans as when conditional-statements are evaluated (such as `if ("test")`), they are evaluated as a boolean
        """

        return True

    @staticmethod
    def test(value: str) -> bool:
        """
        Checks if a given string matches the type of this primitive.

        Args:
            value (str): The string to test.

        Returns:
            bool: True if the string matches the primitive type, False otherwise.
        """
        return True

    @staticmethod
    def new(value: str) -> 'Primitive':
        """
        Parses a string value and returns a new instance of the primitive type.

        Args:
            value (str): The string to parse.

        Returns:
            Primitive: A new instance of the primitive type.
        """
        pass  # Implementation would depend on the specific primitive type

class String(Primitive):
    def __init__(self, value: str = ""):
        """
        Represents a string primitive type.
        """
        super().__init__()

        self.value = String.parse_escape_sequences(value)
        self.real = self.value

    def boolean(self) -> bool:
        return len(self.real) != 0

    @staticmethod
    def parse_escape_sequences(string: str) -> str:
        new_string = ""
        skip = False
        for i,char in enumerate(string):
            if skip:
                skip = False
                continue

            if char == "\\" and string[i-1] != "\\":
                match string[i+1]:
                    case "n":
                        new_string += "\n"
                    case "t":
                        new_string += getGlobal("__TAB_SIZE__") * getGlobal("__TAB_BASE__")
                    case _:
                        new_string += char
                        continue

                skip = True
                continue

            new_string += char
        return new_string

    @staticproperty
    def string_identifier(self) -> str:
        return "string"

    def toString(self) -> str:
        return f"{self.value}"

    @staticproperty
    def match_regex(self) -> str:
        return r"(`(?:(?:\\.|(?:[^\n`\\]))*)`)"

    @staticmethod
    def test(value: str) -> bool:
        return True if re.findall(String.match_regex, value) else False

    @staticmethod
    def new(value: str) -> 'String':
        # assert String.test(value)
        if re.findall(r"^(```).*(```)$", value):
            value = value[3:-3]
        elif value.startswith("`") and value.endswith("`"):
            value = value[1:-1]

        value = String.parse_escape_sequences(value)

        string = String()
        string.value = value

        return string

class Boolean(Primitive):
    def __init__(self):
        """
        Represents a boolean primitive type.
        """
        super().__init__()
        self.value: str = ""
        self.as_bool: bool = False
        self.real = self.as_bool

    @staticproperty
    def string_identifier(self) -> str:
        return "boolean"
    
    def toString(self) -> str:
        return str(self.as_bool)

    def boolean(self) -> bool:
        return self.as_bool

    @staticproperty
    def boolean_regex(self) -> str:
        return r"^(false|true)$"

    @staticmethod
    def test(value: str) -> bool:
        return True if re.findall(Boolean.boolean_regex, value) else False

    @staticmethod
    def new(value: str) -> 'Boolean':
        assert Boolean.test(value)

        boolean = Boolean()
        boolean.value = value
        boolean.as_bool = True if value == "bool" else False
        boolean.real = boolean.as_bool

        return boolean

class Number(Primitive):
    def __init__(self):
        """
        Represents a number primitive type.
        """
        super().__init__()
        self.value: str = ""
        self.as_number: float = 0.0
        self.real = self.as_number

    @staticproperty
    def string_identifier(self) -> str:
        return "number"

    def boolean(self) -> bool:
        return self.as_number == 0
    
    def toString(self) -> str:
        return str(self.as_number)

    @staticproperty
    def number_regex(self) -> str:
        return r"^((\-)?(\d*)(\.?)(\d*)((e|E)(\-|\+)?(\d*)(\.?)(\d+))?)$"

    @staticmethod
    def test(value: str) -> bool:
        return True if re.findall(Number.number_regex, value) else False

    @staticmethod
    def new(value: str) -> 'Number':
        assert Number.test(value)

        number = Number()
        number.value = value
        number.as_number = parse_number(value)
        number.real = number.as_number

        return number

def parse_number(number: str) -> int | float:
    if not re.findall(Number.number_regex, number):
        return False

    if "e" in number:
        return float(number)
    elif "." in number:
        return float(number)
    else:
        return int(number)
    return None