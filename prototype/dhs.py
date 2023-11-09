#################################################################################
###                                                                           ###
###                            [ Module Imports: ]                            ###
###                                                                           ###
#################################################################################

from typing import Type,Literal
import re
import random

#################################################################################
###                                                                           ###
###                   [ HamenScript Symbol Value Encoding ]                   ###
###                                                                           ###
#################################################################################

class HSSV:
    def encode(value: str) -> str:
        return ":".join([x.encode().hex() for x in list(value)])

    def decode(value: str) -> str:
        return "".join([bytes.fromhex(x).decode("utf-8") for x in value.split(":")])

#################################################################################
###                                                                           ###
###                              [ Exceptions: ]                              ###
###                                                                           ###
#################################################################################

class HamenScriptError(BaseException):
    """
    Base exception for a HamenScript interpreter error
    """

class ReadOnlyError(HamenScriptError):
    """
    Attempted to set a value that is read-only
    """

class MemoryAddressError(HamenScriptError):
    """
    Error occurred regarding memory address
    """


################################################################################
###                                                                          ###
###                         [ Common/Helper Types: ]                         ###
###                                                                          ###
################################################################################

class Set:
    def __init__(self, *items) -> None:
        """
        Custom implementation of a set; allows for any data-type
        """
        self._set = list()

        raise NotImplementedError

    def add(self, value: any) -> None:
        if not self.contains(value):
            self._set.append(value)


#################################################################################
###                                                                           ###
###                                [ Memory: ]                                ###
###                                                                           ###
#################################################################################

class TMemoryType:
    """
    Base/parent-class for a memory data-type;

    all memory values are stored as strings but when retrieved are read using a `TMemoryType`
    """

    defaultValue: str = ""
    """ Default value assigned to this """

    typeSignature = "type"
    """ Primitive type signature """

    typeClassIdentifier = "Type"
    """
    Associated prototype class

    All methods & properties of the prototype class use prefixes to denote accessibility :
        "MX_" (public methods)
            such as "MX_zFill()" for string
        "PX_" (public properties) ;
            such as "PX_len" for string

        "MV_" (internal methods)
        "PV_" (internal properties) ;
            the value is stored with the internal property, "V_value"
        
        **************************************************************
        *    These prefixes are NOT written by the user; they are    *
        *   merely to distinguish methods accessible to the reader,  *
        *       and for the primitive abstract implementation        *
        **************************************************************
    """

    @staticmethod
    def testValue(_value: str) -> bool:
        """
        Takes a value (passed from `Memory`) and semantically analyses it with regards to this memory type
        """
        ...

class TInteger(TMemoryType):
    typeSignature = "integer"
    typeClassIdentifier = "Integer"
    defaultValue: str = "0"

    @staticmethod
    def testValue(_value: str) -> bool:
        return True if re.findall(r"^(\d+)$", _value) else False

class TEmptyValue(TMemoryType):
    typeSignature = "empty"
    typeClassIdentifier = "Empty"
    defaultValue: str = ""

    @staticmethod
    def testValue(_value: str) -> bool:
        return False

class TString(TMemoryType):
    typeSignature = "string"
    typeClassIdentifier = "String"
    defaultValue: str = ""

    @staticmethod
    def testValue(_value: str) -> bool:
        return True

class TNull(TMemoryType):
    typeSignature: str = "null"
    typeClassIdentifier: str = "Null"
    defaultValue: str = "null"

    @staticmethod
    def testValue( _value: str) -> bool:
        # A null value doesn't have value; it is ALWAYS `null`;
        #   though there is no reason for "_value" to not be "", even if it is, it will still be null
        return True


class MemoryAddress:
    def __init__(self, address: int = -1) -> None:
        """
        Represents a pointer to a memory address
        """
        self._address: int = address

    @property
    def address(self) -> int:
        return self._address

    @address.setter
    def address(self, address: Type['MemoryAddress'] | int) -> None:
        """
        Relocates this address to the given address;

        this should ONLY be used internally within the `Memory` class
        """
        self._address = address.__int__()

    def __int__(self) -> int:
        return self._address

    def __str__(self) -> str:
        return self._address.__str__()

class Memory:
    def __init__(self):
        """
        Represents a dynamic, modern, RAM-like data structure
        """
        self._memory: list[list[Memory.MemoryValue, MemoryAddress]] = list()
        self._size: int = 0 # Byte-size of entire memory
        self._length: int = 0 # Items in list

    @property
    def size(self) -> int:
        """
        Returns the size of the memory in bytes
        """

        return self._size

    def __str__(self) -> str:
        return "{\n" + "\n".join([f"    {x[0]} -> {x[1].value.__str__()} : {x[1].type.__name__}" for x in self._memory]) + "\n}"

    def _read(self, address: MemoryAddress | int) -> 'Memory.MemoryValue':
        addressIndex = address.__int__()

        assert 0 <= addressIndex < self._length

        assert len(self._memory[addressIndex]) == 2 and self._memory[addressIndex][0] == address, "Internal memory error."

        return self._memory[addressIndex][1]

    def valueAt(self, address: MemoryAddress | int) -> str:
        """
        Reads, then returns the string-value at a memory address

        Raises error if memory address does not exist
        """
        return self._read(address).value

    def sizeAt(self, address: MemoryAddress | int) -> int:
        """
        Returns the size of the value at a given memory address

        Raises error if memory address does not exist
        """
        return self._read(address).size

    def typeAt(self, address: MemoryAddress | int) -> Type[TMemoryType]:
        """
        Reads, then returns the registered type of the value at a memory address

        Raises error if memory address does not exist
        """
        return self._read(address).type

    def append(self, _value: str, _type: TMemoryType) -> MemoryAddress:
        """
        Appends a new value to memory

        Returns a pointer to the new address
        """
        assert _type.testValue(_value), f"Invalid value, '{_value}', for type: '{_type().typeClassIdentifier}'"

        value = Memory.MemoryValue(_value, _type)
        pointer = MemoryAddress(self._length) # Not `-1` because the size will +=1 after the value is added
        self._memory.append([pointer, value])
        self._size += value.size
        self._length += 1

        return pointer

    def writeValue(self, address: MemoryAddress | int, value: str) -> None:
        """
        Writes memory at `address`

        Raises error if memory address does not exist
        """
        addressIndex = address.__int__()
        assert 0 <= addressIndex < self._length

        _type = self.typeAt(address)
        assert _type.testValue(value), f"Invalid value, '{value}', for type: '{_type().typeClassIdentifier}'"

        self._size -= self.sizeAt(address)

        self._memory[addressIndex][1].value = value

        self._size += self.sizeAt(address)

    def writeType(self, address: MemoryAddress | int, type: Type[TMemoryType]) -> None:
        """
        Writes the type at `address`

        Raises error if memory address does not exist
        """
        addressIndex = address.__int__()
        assert 0 <= addressIndex < self._length
        if self.typeAt(address) is not TEmptyValue:
            assert type.testValue(self.valueAt(address)), f"Invalid value, '{self.valueAt(address)}', for type: '{type().typeClassIdentifier}'"
        else:
            self._memory[addressIndex][1].type = type
            self.writeValue(address, type.defaultValue)
            return

        self._memory[addressIndex][1].type = type

    def delete(self, address: MemoryAddress | int) -> None:
        """
        Removes something from memory

        Raises error if memory address does not exist
        """
        addressIndex = address.__int__()
        assert 0 <= addressIndex < self._length

        self._size -= self.sizeAt(address)

        self._memory = [*self._memory[:addressIndex], *self._memory[1+addressIndex:]]
        for i in range(addressIndex, self._length - 1):
            self._memory[i][0].address -= 1

    def clearValue(self, address: MemoryAddress | int) -> None:
        addressIndex = address.__int__()
        assert 0 <= addressIndex < self._length
        self._memory[addressIndex][1].setEmpty(True)

    class MemoryValue:
        def __init__(self, _value: str = None, _type: TMemoryType = None) -> None:
            """
            Represents an entry value in memory;

            This should ONLY be used abstractly by the `Memory` class

            string-value representation is "_value" then its type is "_type"
            """

            # Ensure specified `_value` and `_type`
            assert all((_value, _type, isinstance(_value, str), isinstance(_type, (TMemoryType, type(TMemoryType))))), "Must specify value [as `str`] and type [as `TMemoryType`] for memory value"

            # Add value and type
            self._empty: bool = False
            self._value: str = _value
            self._type: TMemoryType = _type
            self._size: int = len(_value)

        def setEmpty(self, value: bool) -> None:
            assert type(value) is bool
            if value:
                self._value = ""
                self._size = 0
                self._type = TEmptyValue

            self._empty = value

        @property
        def size(self) -> int:
            return self._size

        @size.setter
        def size(self, value: int) -> None:
            assert type(value) is int
            assert 0 <= value

            self._size = value

        @property
        def type(self) -> Type[TMemoryType]:
            if self._empty: return TEmptyValue
            return self._type
        
        @type.setter
        def type(self, value: TMemoryType) -> None:
            self.setEmpty(False)

            assert isinstance(value, type(TMemoryType))
            self._type = value

        @property
        def value(self) -> str:
            return self._value

        @value.setter
        def value(self, value: str) -> None:
            """
            Sets the value associated to this MemoryClass instance;

            NOTE: Changing this value does not affect the value stored in memory:
                it should only be changed internally within the `Memory` class
            """

            # Ensure that the value is a string
            assert isinstance(value, str) and self._type

            self._size = len(value)
            self._value = value

        def __str__(self) -> str:
            return self._value


#################################################################################
###                                                                           ###
###                            [ Runtime Common: ]                            ###
###                                                                           ###
#################################################################################

class Runtime:
    def __init__(self) -> None:
        """
        Defines a global variable with attributes associated with the current runtime

        Includes stuff like runtime memory so when the interpreter is terminated, a garbage collector is not necessary
        """

        self.memory: Memory = Memory()


#################################################################################
###                                                                           ###
###                          [ Compiler -> Tokens: ]                          ###
###                                                                           ###
#################################################################################

class LiteralList:
    def __init__(self, *items: str, separator: str = r"|"):
        """
        A list of regular-expression literal strings; used for the `__all__` attribute of a Token
        """
        self._items = list(items)
        self.separator = separator

    def __str__(self, *, sep: str = r"|") -> str:
        return self.separator.join(self._items)

    def join(self, sep: str = None) -> str:
        if not sep:
            sep = self.separator

        return sep.join(self._items)

    def __iter__(self) -> list:
        return self._items

    def __contains__(self, value: str) -> bool:
        return any([re.findall(r"^" + x + r"$", value) for x in self._items])

    def test(self, value: str) -> bool: return self.__contains__(value)


class Token:
    """
    Base token; split into three types:
    1. Symbol: a variable, namespace, function, etc;
        variables are defined with the "$" prefix; they should not be placed inside value brackets ( `{ ... }` )
    """

    tokenName: str = "TOKEN"
    """ Uppercase name for this token; used in Semantic Analysis and Execution """

    tokenValue: str = None
    """ Value assigned to this token; not applicable for all tokens: only those like Variable or one that hold specific values """

    __all__: LiteralList = LiteralList()
    """ All direct literal strings of this token """

class Tokens:
    class Values:
        class Variable(Token):
            """
            Variable name; denoted with "$" prefix

            `value` should not have "$" prefix
            """
            tokenName = "VARIABLE"
            regex: str = r"^([a-zA-Z_]+[a-zA-Z0-9_]*)$"

        class String(Token):
            """
            String value; denoted with "/" prefix and suffix
            """
            tokenName = "STRING"
            regex: str = r"^(\/.*\/)$"


    class Symbol(Token):
        """
        Function, variable, namespace, etc
        """
        tokenName = "SYMBOL"

    class Delimiter(Token):
        """
        ">>", "::", etc
        """

        tokenName = "DELIMITER"
        __all__ = LiteralList(r"&&", r"<<\|", r"\|>>", r">>", r"::")

class NS:
    __all__: tuple = ()
    class Namespace:
        __all__: tuple = ()

    class Function: pass

class DEL(NS.Namespace):
    class EOL(NS.Function): """ End-of-Line """
    class SOL(NS.Function): """ Start-of-Line """
    class SOC(NS.Function): """ Start-of-Comment """
    class EOC(NS.Function): """ End-of-Comment """

class DEC(NS.Namespace):
    class VAR(NS.Function): """ Declare Variable """
    class FCN(NS.Function): """ Declare Function """
    class PRO(NS.Function): """ Declare Procedure """

class MUT(NS.Namespace):
    class STO(NS.Function): """ Mutate / Store """
    class REM(NS.Function): """ Mutate / Remove """
    class CTO(NS.Function): """ Mutate / Cast To """
    class CLR(NS.Function): """ Mutate / Clear Value """
    class ASN(NS.Function): """ Mutate / Assign Value """

class ACC(NS.Namespace):
    class PRV(NS.Function): """ Access Modifier / Private """
    class PUB(NS.Function): """ Access Modifier / Public """

class SCO(NS.Namespace):
    class CST(NS.Function): """ Scope / Const """
    class LET(NS.Function): """ Scope / Let """
    class VAR(NS.Function): """ Scope / Var """
    class TMP(NS.Function): """ Scope / Temp """

class TYP(NS.Namespace):
    class INT(NS.Function): """ Type / Integer """
    class FLO(NS.Function): """ Type / Float """
    class STR(NS.Function): """ Type / String """
    class BOL(NS.Function): """ Type / Boolean """
    class NUL(NS.Function): """ Type / Null """
    class UND(NS.Function): """ Type / Undefined """
    class NAN(NS.Function): """ Type / NaN """

pickNamespaceFunctions = lambda ns : tuple([attr for attr in [getattr(ns, x) for x in dir(ns)] if type(attr) is type and len(attr.__name__) == 3 and all([x.isupper() for x in list(attr.__name__)])])

NS.__all__ = (DEL, DEC, MUT, ACC, SCO, TYP)
DEL.__all__ = pickNamespaceFunctions(DEL)
DEC.__all__ = pickNamespaceFunctions(DEC)
MUT.__all__ = pickNamespaceFunctions(MUT)
ACC.__all__ = pickNamespaceFunctions(ACC)
SCO.__all__ = pickNamespaceFunctions(SCO)
TYP.__all__ = pickNamespaceFunctions(TYP)

class Line:
    def __init__(self, raw_line: str = None):
        pass

#################################################################################
###                                                                           ###
###                               [ Compiler: ]                               ###
###                                                                           ###
#################################################################################

class Tag:
    def __init__(self, token: Token) -> None:
        """
        Used explicitly by `Compile.semanticAnalysis( ... )`
        """
        self.name = token.tokenName
        self.value = token.tokenValue

        self.target = None
        """ For special use """

class Compile:
    def __init__(self, code: str) -> None:
        """
        Steps to compiler:
        1. Lexical analysis;
            done with `self.lexicalAnalysis(...) -> list[Line]`
        """

        self.code = code.strip()
        self.code = self.lexicalAnalysis(self.code)
        self.code = self.semanticAnalysis(self.code)

    def lexicalAnalysis(self, rawCode: str) -> list[list[Token]]:
        """
        Tokenize `rawCode`
        """

        # Step one: separate the comments:
        code = re.split(r"^(\s*\/\/\s+.*)|(.*)", rawCode)
        code = [x for x in code if x and x.strip()]

        # Step two: separate the values "{ ... }"
        #   all content inside the values should be encoded with HamenScript String Encoding
        new_code = []
        for term in code:
            if term.strip().startswith("// "):
                new_code.append(term)
                continue

            values = [x.strip() for x in re.split(r"({.*?})", term) if x and x.strip()]
            values = [item for x in values for item in (re.split(
                r"(" + Tokens.Delimiter.__all__.join() + r"|[a-zA-Z0-9]+)",
                x
            ) if not re.findall(r"({.*?})", x) else [x])]
            values = [self.identifyToken(x) for x in values if x and x.strip()]

            new_code.append(values)

        return new_code

    def semanticAnalysis(self, codeLines: list[list[Token]]) -> None:
        error = lambda message : f"SemanticSyntaxError: {message}"

        for line in codeLines:
            assert len(line) >= 3, "Line too short."
            assert "::".join(x.tokenName for x in line[:3]) == "SYMBOL::DELIMITER::SYMBOL"

            lineType = line[2].tokenValue
            assert lineType in ["SOL", "SOC"], error(f"Invalid line type: '{lineType}'")
            assert "E" + lineType[1:] == line[-1].tokenValue, error(f"Line terminated with different opening type: '{lineType}' ... '{line[-1].tokenValue}'")

            tags = [Tag(x) for x in line]
            skip = 0
            for i,tag in enumerate(tags):
                if skip:
                    skip -= 1
                    continue

                tag: Tag

                # Access namespace:
                if tag.value == "::":
                    # Find accessed namespace and function;
                    #   1. `tagNS`
                    #   2. `_`
                    #   3. `tagFn`
                    #   
                    #    1  _ 3
                    #   DEL::SOL
                    tagNS,_,tagFn = tags[i-1:i+2]

                    # Ensure namespace exists:
                    assert tagNS.value in [x.__name__ for x in NS.__all__], f"Namespace does not exist: '{tagNS}'"

                    # Get the namespace class (type: `NS.Namespace`):
                    tagNS.target = [x for x in NS.__all__ if x.__name__ == tagNS.value][0]

                    # Ensure the function exists in the namespace:
                    assert tagFn.value in [y for y in [x.__name__ for x in tagNS.target.__all__]], f"Function, '{tagFn.value}', does not exist namespace, '{tagNS.value}'"

                    # Get the function class (type: `NS.Function`):
                    tagFn.target = [x for x in tagNS.target.__all__ if x.__name__ == tagFn.value][0]

                    # 

    def newToken(self, _value: str, _type: Token) -> Token:
        t = _type()
        t: Token
        t.tokenValue = _value

        return t

    def identifyToken(self, token: str) -> Token:
        token = token.strip()

        # Token is delimiter (e.g. "::", ">>", etc)
        if token in Tokens.Delimiter.__all__:
            return self.newToken(token, Tokens.Delimiter)

        # Token is { ... }
        elif re.findall(r"^(\{[\s\S]*\})$", token):
            # Get the contents of the value
            _content = re.match(r"^\{\s*([\s\S]*)\s*\}$", token)
            _content = _content.group(1)

            # Match further the type of this value;
            #   examples include: variables with "$", strings with "/.../", etc.
            # 
            # Token is a Variable:
            if re.findall(r"^(\$" + Tokens.Values.Variable.regex.lstrip(r"^").rstrip(r"$") + r")$", _content):
                return self.newToken(_content.lstrip("$"), Tokens.Values.Variable)

            # Token is an Encrypted value:
            elif re.findall(r"^(\/.*\/)$", _content.strip()):
                _content = _content.strip().strip("/").strip()
                return self.newToken(HSSV.decode(_content), Tokens.Values.String)

            # 
            else:
                assert False, f"Invalid value: '{token}'"

        # Token follows variable name (e.g. "VAR", "DEL", etc)
        elif re.findall(Tokens.Values.Variable.regex, token):
            return self.newToken(token, Tokens.Symbol)

        else:
            assert False, str(_content)

Compile("""
DEL::SOL <<|    DEC::VAR >> {$x} >> SCO::LET >> TYP::INT >> { /31:33/ }    |>> DEL::EOL
""".strip())

