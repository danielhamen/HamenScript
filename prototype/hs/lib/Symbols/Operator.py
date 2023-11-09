from enum import Enum

from hs.lib.staticproperty import staticproperty
from hs.lib.Symbols.Tokens import Token

class Operator(Token):
    def __init__(self, operator: str = None):
        self.operator: str = operator
        self.classification: str = Classifications.match(operator)

        # Define this as each primitive type has the `self.value` property
        self.value: str = operator

    def boolean(self) -> bool:
        return self.operator == "+"

    @staticproperty
    def string_identifier(self) -> str:
        return "operator"

    def __str__(self) -> str:
        return self.operator

class Classifications(Enum):
    GroupOperators = ["(", ")", "[", "]", "{", "}"]
    AssignmentOperators = ["=", "+=", "-=", "*=", "/=", "%=", "**=", "++", "--"]
    ComparisonOperators = ["==", "===", "!=", "!==", "<=", "<", ">", ">="]
    ArithmeticOperators = ["+", "-", "*", "**", "%", "/"]
    LogicalOperators = ["!", "&&", "||"]
    SpecialOperators = ["...", ",", "?", "!"]

    def match(operator: str) -> str or None:
        classifications = Classifications
        if operator in classifications.GroupOperators.value:
            return "GROUP"
        elif operator in classifications.AssignmentOperators.value:
            return "ASSIGNMENT"
        elif operator in classifications.ComparisonOperators.value:
            return "COMPARISON"
        elif operator in classifications.ArithmeticOperators.value:
            return "ARITHMETIC"
        elif operator in classifications.LogicalOperators.value:
            return "LOGICAL"
        elif operator in classifications.SpecialOperators.value:
            return "SPECIAL"

        return None