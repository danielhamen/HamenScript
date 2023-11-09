from itertools import groupby
import sys
import textwrap
from termcolor import colored
import colorama
import string
import re

import hs.__init__ as hs
from hs.Globals import *

Types = hs.Symbols.Types

class Operands:
    def XADD(a: hs.Symbols.Types.Primitive, b: hs.Symbols.Types.Primitive) -> hs.Symbols.Types.Primitive:
        """
        `+` operator
        """

        ans = None
        if all([type(x) is Types.Number for x in (a, b)]):
            a: Types.Number
            b: Types.Number

            ans = Types.Number.new(a.as_number + a.as_number)
        else:
            a = a.toString()
            b = b.toString()

            ans = Types.String(a + b)

        assert ans
        return ans

    def XSUBTRACT(a: hs.Symbols.Types.Primitive, b: hs.Symbols.Types.Primitive) -> hs.Symbols.Types.Primitive:
        """
        `-` operator
        """

        ans = None
        if all([type(x) is Types.Number for x in (a, b)]):
            a: Types.Number
            b: Types.Number

            ans = Types.Number.new(a.as_number - a.as_number)

        assert ans
        return ans

# ASSIGNMENT_OPERATORS = ["=", "+=", "-=", "/=", "*=", "**=", "%="]
# COMPARISON_OPERATORS = ["==", "!=", "===", "!==", "<", ">", "<=", ">="]
# ARITHMETIC_OPERATORS = ["+", "-", "*", "/", "%"]
# LOGICAL_OPERATORS = ["&&", "||", "!"]
# GROUP_OPERATORS = ["(", ")", "[", "]", "{", "}"]
# ALPHABET = "QWERTYUIOPSDFGJKLXCVBNMZ".split()
# NUMBERS = "1234567890".split()
# TAB_SIZE = 4
# TAB = " " * TAB_SIZE

def raise_error(_message: str = "", error_type: str = "", *, reference: str = None, **kwargs) -> None:
    def wrap_error(message: str, pre_tab: int) -> str:
        tab = " " * pre_tab
        lines = [tab]
        width = os.get_terminal_size().columns
        for i,char in enumerate(message):
            if len(lines[-1]) == width or char == "\n":
                lines.append(tab + ("" if re.findall(r"\s", char) else char))
            else:
                lines[-1] += char

        return "\n".join(lines).lstrip()

    title = content = message = None
    tab = " " * 4
    if reference:
        title = hs.ErrorReferences.get(reference)[0]
        content = hs.ErrorReferences.get(reference)[1](**kwargs)
        message = [
            colored(f"(REF:{reference}) ~ ", "red"),
            colored(title, "red", attrs=["bold", "dark"]),
            colored(f": ", "red"),
            colored(wrap_error(content, (4 + len(title) + len(": ") + len(f"(REF:{reference}) ~ "))), "red", attrs=["dark"])
        ]

    else:
        title = error_type
        content = _message
        message = [
            colored(title, "red", attrs=["bold", "dark"]),
            colored(f": ", "red"),
            colored(wrap_error(content, (4 + len(title) + len(": "))), "red", attrs=["dark"])
        ]

    message = "".join(message)
    message = colored(f"\n\nTraceback, most recent call:\n", "red") + tab + message

    print(message)

    hs.ExecutionControl.END_CODE()

class LineRange:
    def __init__(self, line_number: int, column_start: int, column_end: int):
        """
        Represents a range of line and column numbers in the source code.
        Used for tracking where a token is found in the source code.

        Args:
            line_number (int): The line number in the source code.
            column_start (int): The starting column number.
            column_end (int): The ending column number.
        """
        self.line_number = line_number
        self.column_start = column_start
        self.column_end = column_end

class Interpret:
    def __init__(self, code: str, globals: hs.Common.GlobalList = hs.Common.GlobalList(), safe_environment: bool = False):
        self.globals: hs.Common.GlobalList = globals
        self.code: str = code
        self.safe_environment = safe_environment # Inside a try/catch statement
        self.status = False

        self.tokens = self.tokenize(self.code)
        if not self.status:
            self.execute_code(self.tokens)

    def execute_code(self, _tokens: list):
        tokens = _tokens
        for i,line in enumerate(_tokens):
            if any([not isinstance(x, hs.Symbols.Tokens.Token) for x in line]):
                line = [x for x in line[0] if x]

                for term_index,term in enumerate(line):
                    if re.findall(r"^\{.*\}$", term):
                        continue

                    content = line[term_index+1][1:-1]

                    # Match function:
                    if re.findall(r"^function\W", term):
                        fn = hs.Symbols.Tokens.Function()
                        match = re.match(hs.Symbols.Tokens.Function.regex, term)
                        kwd,name,args = match.group(1, 2, 3)
                        fn.name = name
                        fn.arguments = fn.parse_arguments(args)

                        if i != 0 and _tokens[i-1] and len(_tokens[i-1]) != 0 and type(_tokens[i-1][0]) is hs.Symbols.Tokens.Decorator:
                            decorator = _tokens[i-1][0]
                            decorator: hs.Symbols.Tokens.Decorator

                        fn.decorators.append(decorator)

                    # Match if-statement:
                    elif re.findall(r"^if\W", term):
                        match = re.match(r"^(if).*(\(.*\))", term)
                        kwd,condition = match.group(1, 2)

                        if condition:
                            Interpret(content, self.globals)

                    # Match elif-statement:
                    elif re.findall(r"^elif\W", term):
                        match = re.match(r"^(elif).*(\(.*\))", term)
                        kwd,condition = match.group(1, 2)

                        if not re.findall(r"^if\W", line[0]):
                            if self.safe_environment: self.status = "ControlFlowError";return
                            raise_error("`elif` statements cannot be independent to a condition tree; ensure you have an `if` statement", "ControlFlowError")

                        if condition:
                            Interpret(content, self.globals)

                    # Match else-statement:
                    elif re.findall(r"^else", term):
                        # Automatically execute the next code as if any of the statements above were true, the loop would break and never reach here

                        if not re.findall(r"^if\W", line[0]):
                            if self.safe_environment: self.status = "ControlFlowError";return
                            raise_error("`elif` statements cannot be independent to a condition tree; ensure you have an `if` statement", "ControlFlowError")

                        Interpret(content, self.globals)

                    # Match try-statement:
                    elif re.findall(r"^(try)", term):
                        # We should do nothing here as the code is interpreted inside the `catch` condition
                        pass

                    # Match catch-statement:
                    elif re.findall(r"^(catch)", term):
                        if line[0] != "try":
                            if self.safe_environment: self.status = "MisplacedCatchError";return
                            raise_error(reference = "x0010")

                        m = Interpret(content, self.globals, safe_environment=True)
                        if m.status:
                            pass

                    # Unknown:
                    else:
                        print("ERROR: " + term)

                continue

            tokens = line
            line = ":".join([x.string_identifier for x in line])

            if not line:
                continue

            if re.findall(r"^((const|let):.*)", line):
                if len(tokens) <= 3:
                    if self.safe_environment: self.status = "SyntaxError";return
                    raise_error("Not enough terms", "SyntaxError")
                if isinstance(tokens[1], hs.Symbols.Tokens.Keyword):
                    if self.safe_environment: self.status = "x0003";return
                    raise_error(reference="x0003", kwd = tokens[1].token_name.lower())
                elif type(tokens[1]) is not hs.Symbols.Tokens.Variable:
                    if self.safe_environment: self.status = "x0008";return
                    raise_error(reference="x0008", variable_name = tokens[1].toString())

                declare,variable,operator,*value = tokens[0:3] + tokens[3:]
                value = self.evaluate_values(value)
                declare: hs.Symbols.Tokens.Keywords.KLet if declare == "let" else hs.Symbols.Tokens.Keywords.KConst
                variable: hs.Symbols.Tokens.Variable
                operator: hs.Symbols.Operators.Operator
                if operator.classification != hs.Symbols.Operators.Classifications.match("="):
                    if self.safe_environment: self.status = "x0001";return
                    raise_error(reference="x0001")
                elif self.globals.contains(variable.name):
                    if self.safe_environment: self.status = "x0002";return
                    raise_error(reference="x0002")
                elif variable.name in hs.Symbols.Tokens.ReservedKeywords:
                    if self.safe_environment: self.status = "x0003";return
                    raise_error(reference="x0003", kwd = variable.name)

                self.globals.set(variable.name, key = variable, value = value.value, type = type(value), scope = declare.token_name.upper())

            elif re.findall(r"^stdout", line):
                if len(tokens) != 2:
                    if self.safe_environment: self.status = "x0004";return
                    raise_error(reference="x0004")

                kwd,value = tokens[0],tokens[1]
                value = self.evaluate_values([value])
                if value: self.stdout(value)

            elif re.findall(r"^variable:operator:.*", line):
                variable,operator,value = tokens[0],tokens[1],tokens[2:]
                variable: hs.Symbols.Tokens.Variable
                operator: hs.Symbols.Operators.Operator
                value = self.evaluate_values(value)
                if operator.classification != hs.Symbols.Operators.Classifications.match("="):
                    if self.safe_environment: self.status = "x0001";return
                    raise_error(reference="x0001")
                if not self.globals.contains(variable.name):
                    if self.safe_environment: self.status = "x0005";return
                    raise_error(reference="x0005", variable_name = variable.name)

                entry = self.globals.get(variable.name)
                entry: hs.Common.GlobalEntry
                if entry.scope == "CONST":
                    if self.safe_environment: self.status = "x0006";return
                    raise_error(reference="x0006", variable_name = variable.name)

                if entry.strict and not isinstance(value, entry.type):
                    if self.safe_environment: self.status = "x0007";return
                    raise_error(
                        reference="x0007",
                        variable_name = variable.name,
                        variable_type = value.string_identifier,
                        target_type = entry.type.string_identifier
                    )

                self.globals.set(variable.name, value = value)
            
            elif line == "decorator":
                continue

            else:
                print(line)
                pass

        hs.ExecutionControl.END_CODE()

    def stdout(self, value: Types.String) -> None:
        sys.stdout.write("Main.hs >> " + value.value)
        if value.value.endswith("\n"):
            self.stdflush()

    def stdflush(self) -> None:
        sys.stdout.flush()

    def evaluate_values(self, values: list) -> hs.Symbols.Types.Primitive:
        """
        Evaluates `values` to a single, primitively-parsed value
        """

        if len(values) == 1:
            value = values[0]
            if isinstance(value, hs.Symbols.Tokens.Variable):
                value: hs.Symbols.Tokens.Variable
                if not self.globals.get(value.name):
                    if self.safe_environment: self.status = "x0009";return
                    raise_error(reference="x0009", variable_name = value.name)
                value = self.globals.get(value.name)
                value: hs.Common.GlobalEntry
                value = value.type.new(value.value)

            return value

        raise NotImplementedError

    def tokenize(self, code: str):
        string_pattern = hs.Symbols.Types.String.match_regex

        depth = { "(": 0, "[": 0, "{": 0 }
        depth_size = lambda d : d["("] + d["["] + d["{"]
        flip_operator = lambda op : "{" if op == "}" else ("[" if op == "]" else ("(" if op == ")" else None))

        parts = re.split(string_pattern, code)

        tokenized_lines = [""]
        for part in parts:
            if not part:
                continue

            if hs.Symbols.Types.String.test(part) and depth["{"] == 0 and depth["("] == 0:
                tokenized_lines.append([tokenized_lines[-1], hs.Symbols.Types.String.new(part)])
                del tokenized_lines[-2]
                tokenized_lines.append("")

                continue

            part = re.sub(r"(?<=[-!$%^&*()_+|~=`{}\[\]:\";'<>?,.\/])(\s+)(?=\w)|(?!\w)(\s+)(?!\w)", "", part)
            for i,char in enumerate(part):
                if char == "\n":
                    if re.findall(r"[a-zA-Z0-9]$", part[:i].strip()) and re.findall(r"^[a-zA-Z0-9]", part[i:].strip()):
                        tokenized_lines.append("")

                    continue

                if char in "()[]":
                    f_char = flip_operator(char)
                    if f_char:
                        depth[f_char] += 1
                    else:
                        depth[char] -= 1

                if char == "{":
                    depth["{"] += 1
                elif char == "}":
                    depth["{"] -= 1

                    if depth["{"] == 0:
                        tokenized_lines[-1] += char
                        continue

                if depth_size(depth) == 0 and char == ";":
                    tokenized_lines.append("")
                    continue

                tokenized_lines[-1] += char

        tokenized_lines = [x for x in tokenized_lines if x]

        def includes_depth(_code: str) -> bool:
            _code = re.split(hs.Symbols.Types.String.match_regex, _code)
            _code = [x for x in _code if x]
            for term in _code:
                if not hs.Symbols.Types.String.test(term):
                    if "{" in term:
                        return True
            return False

        for line_index,line in enumerate(tokenized_lines):
            # TODO: Implement remove comments
            if type(line) is str: line = [line]
            line = [x.strip() if type(x) is str else x for x in line]

            new_line = []
            for term in line:
                if isinstance(term, hs.Symbols.Types.String):
                    new_line.append(term)
                    continue

                # Remove comments:
                term = re.sub(getGlobal("__ML_COMMENTS__"), "", term)
                term = re.sub(getGlobal("__SL_COMMENTS__"), "", term)

                if includes_depth(term):
                    _terms = []
                    terms = re.split(Types.String.match_regex, term)
                    for term in terms:
                        if term.startswith("`") and term.endswith("`"):
                            _terms.append(term)
                            continue

                        term: str
                        _terms += re.split(r"(\{|\})", term)
                    terms = _terms
                    _terms = []
                    _depth = 0
                    for term in terms:
                        if term == "{":
                            _depth += 1

                            if _depth == 1:
                                _terms.append("")
                        elif term == "}":
                            _depth -= 1
                            _terms[-1] += term
                            continue

                        if _depth == 0:
                            _terms.append(term)
                        else:
                            _terms[-1] += term
                    terms = _terms
                    new_line.append(terms)
                else:
                    new_line += re.split(r"(?![_a-zA-Z0-9])(\S)|\s", term)

            new_line = [x for x in new_line if x]
            line = new_line

            # Line includes decorator:
            if line[0] == "@":
                if len(line) != 2:
                    if self.safe_environment: self.status = "DecorationError";return
                    raise_error(f"Invalid syntax for decorator: \"{line}\"", "DecoratorError")

                line = ["".join(line)]

            # Line includes "...":
            elif any(line[i:i+len(list("..."))] == list("...") for i in range(len(line) - len(list("...")) + 1)):
                line = ["..." if k == "." else k for k, g in groupby(line)]

            # Tokenize line:
            for i,token in enumerate(line):
                if type(token) is str:
                    token = token.strip()

                    # Match keyword:
                    if token in hs.Symbols.Tokens.ReservedKeywords:
                        token = hs.Symbols.Tokens.MatchKeyword(token)()

                    # Match boolean:
                    elif hs.Symbols.Types.Boolean.test(token):
                        token = hs.Symbols.Types.Boolean.new(token)

                    # Match number:
                    elif hs.Symbols.Types.Number.test(token):
                        token = hs.Symbols.Types.Number.new(token)

                    # Match decorator:
                    elif hs.Symbols.Tokens.Decorator.test(token):
                        token = hs.Symbols.Tokens.Decorator(re.match(hs.Symbols.Tokens.Decorator.regex, token).group(0))

                    # Match variable:
                    elif re.findall(r"[a-zA-Z_][a-zA-Z_0-9]*", token):
                        if not re.findall(r"^([a-zA-Z_]+)([a-zA-Z_0-9]*)$", token):
                            if self.safe_environment: self.status = "x0008";return
                            raise_error(reference="x0008", variable_name = token)

                        token = hs.Symbols.Tokens.Variable(token)

                    # Match operator:
                    elif hs.Symbols.Operators.Classifications.match(token) or token in ["?", ":", ","]:
                        token = hs.Symbols.Operators.Operator(token)

                    else:
                        # Match depth:
                        if includes_depth("".join([x.__str__() for x in line])):
                            continue

                        if self.safe_environment: self.status = "SyntaxError";return
                        raise_error(f"Invalid token: \"{token}\"", "SyntaxError")

                elif type(token) is list:
                    for term_index in range(0, len(token), 2):
                        if len(token) <= term_index + 1: break
                        raw_term,content = token[term_index],token[term_index+1]
                        term = re.sub(r"[^a-zA-Z]+", ":", raw_term)
                        term = term.strip(":")
                        match = term.startswith
                        Keywords = hs.Symbols.Tokens.Keywords

                        keyword = None
                        if match("if"): keyword = Keywords.KIf
                        elif match("elif"): keyword = Keywords.KElif
                        elif match("else"): keyword = Keywords.KElse
                        elif match("try"): keyword = Keywords.KTry
                        elif match("catch"): keyword = Keywords.KCatch
                        elif match("case"): keyword = Keywords.KCase
                        elif match("class"): keyword = Keywords.KClass
                        elif match("constructor"): keyword = Keywords.KConstructor
                        elif match("defer"): keyword = Keywords.KDefer
                        elif match("do"): keyword = Keywords.KDo
                        elif match("enum"): keyword = Keywords.KEnum
                        elif match("finally"): keyword = Keywords.KFinally
                        elif match("for"): keyword = Keywords.KFor
                        elif match("function"): keyword = Keywords.KFunction
                        elif match("interface"): keyword = Keywords.KInterface
                        elif match("match"): keyword = Keywords.KMatch
                        elif match("namespace"): keyword = Keywords.KNamespace
                        elif match("switch"): keyword = Keywords.KSwitch
                        elif match("throw"): keyword = Keywords.KThrow
                        elif match("watch"): keyword = Keywords.KWatch
                        elif match("with"): keyword = Keywords.KWith
                        elif match("while"): keyword = Keywords.KWhile
                        else:
                            if self.safe_environment: self.status = "SyntaxError";return
                            raise_error(f"Misuse of `{term}` keyword; {line}", "SyntaxError")

                        keyword: hs.Symbols.Tokens.Keyword
                        keyword = keyword.parse(token)

                line[i] = token

            tokenized_lines[line_index] = line

        # Merge operators (e.g. ["+", "="] -> ["+="])
        for line_index,line in enumerate(tokenized_lines):
            operator_stack = []
            is_operator = False
            new_line = []
            i = 0

            # Go through each token in the line
            while i < len(line):
                token = line[i]

                # The iter token is an operator
                if isinstance(token, hs.Symbols.Operators.Operator) and token.classification != hs.Symbols.Operators.Classifications.GroupOperators.value:
                    if is_operator:
                        operator_stack.append(token)
                    else:
                        operator_stack = [token]
                        is_operator = True

                # The last token was an operator; this checks whether the current token is not an operator as if it is not, it should not be merged
                if (len(operator_stack) != 0 and i + 1 >= len(line)) or (is_operator and not isinstance(token, hs.Symbols.Operators.Operator)):
                    is_operator = False
                    operator = hs.Symbols.Operators.Operator("".join([x.operator for x in operator_stack]))
                    operator_stack = []
                    i -= len(operator_stack)

                    if type(token) is not hs.Symbols.Operators.Operator:
                        new_line.append(token)
                    else:
                        new_line.append(operator)

                else:
                    new_line.append(token)

                i += 1

            tokenized_lines[line_index] = new_line

        return tokenized_lines

if __name__ == "__main__":
    # Get, and read input file
    code: str = None
    input_file: str = r"prototype\Main.hs"
    with open(input_file) as file:
        code = file.read()
    assert code, f"Error fetching the code..."

    # Log code interpretation
    # This has to start before `#PRAGMA` collection as it will reset all globals
    hs.ExecutionControl.START_CODE()

    # Search for #PRAGMA definitions:
    match_pragma = r"^(#PRAGMA)\s*::\s*([a-zA-Z_]+[a-zA-Z_0-9]*)\s*>>\s*(.*);$"
    code = code.split("\n")
    for i,line in enumerate(code):
        line = line.strip()
        if not re.findall(match_pragma, line):
            code = code[i:]
            break

        pragma,key,value = re.findall(match_pragma, line)[0]
        if not getGlobal(key):
            raise_error(f"Invalid syntax for pragma declaration; the specified key `{key}` does not exist.", "IllegalPragmaDeclaration")

            hs.ExecutionControl.END_CODE()

        if hs.Symbols.Types.String.test(value):
            value = hs.Symbols.Types.String.new(value).real
        elif hs.Symbols.Types.Number.test(value):
            value = hs.Symbols.Types.Number.new(value).as_number
        elif hs.Symbols.Types.Boolean.test(value):
            value = hs.Symbols.Types.Boolean.new(value).as_bool
        else:
            raise_error(f"Invalid syntax for pragma declaration; the specified value should be a string, number, or boolean", "IllegalPragmaDeclaration")
            hs.ExecutionControl.END_CODE()

        setGlobal(key, value)

    code = "\n".join(code)

    _globals = hs.Common.GlobalList()

    Interpret(code, _globals)

"""
Ideas:
- Rounding operator: use `9.923480 -> %3` as `round(9.923480, 3)`
- Use "..." for ranges of numbers: `[3...6]` as `[3, 4, 5]`
- Inline suffix decorators: `const x = calculateBigArray() @cache`
- Watch for variable changes:
```
let x = 13;
watch x with (oldValue, newValue) {};
```

- Custom types (not data types) to follow trends with regex -- for validation:
```
type TopLevelDomain: string = r`\.(com|ca|org)`gi;
type Domain: string = r`^(gmail)$`gi;
type Email: string = [r`[\S]{4,}\@`, Domain, r`\.`, TopLevelDomain];
```

- Keyword-functions: use functions as keywords (e.g. `round 3.9,3`)

- Pseudo keyword for documentation purposes:
```
const myFunction = () => {
    ...
};

pseudo myFunction {
    
};
```

- Defer keyword:
```
const myFunction = () => {
    throw `Error`;

    defer {
        console.log(`Executed`) // This will execute as it is defered; if an error occurs inside this, it will be ignored and continue
    };
};
```

- Privileged functions to access internal keywords:
```
const privileged log = () => {
    stdout `Hello World!`; // No error
};

stdout `Hello World!`; // Error as `stdout` keyword is not accessible in this unprivileged context
```
"""