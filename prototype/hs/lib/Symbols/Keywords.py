import re

from hs.lib.Common import Common
from hs.lib.Symbols.Tokens import Token
from hs.lib.staticproperty import staticproperty

class Keyword(Token):
    def __init__(self, token_name: str = "KEYWORD"):
        """
        Represents a keyword token in the source code.
        """
        super().__init__()
        self.token_name = token_name or "KEYWORD"
        self.globals: Common.GlobalList = Common.GlobalList()

    @staticproperty
    def string_identifier(self) -> str:
        return "keyword"

    def toString(self) -> str:
        return self.token_name.lower()

    @staticmethod
    def parse(value: str) -> 'Keyword':
        return Keyword()

class Keywords:
    class KVolatile(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "VOLATILE"   

        @staticproperty
        def string_identifier(self) -> str:
            return "volatile"


    class KGlobal(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "GLOBAL"   

        @staticproperty
        def string_identifier(self) -> str:
            return "global"


    class KClass(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "CLASS"

        @staticproperty
        def string_identifier(self) -> str:
            return "class"


    class KFrom(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "FROM"

        @staticproperty
        def string_identifier(self) -> str:
            return "from"


    class KAssertle(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "ASSERTLE"

        @staticproperty
        def string_identifier(self) -> str:
            return "assertle"


    class KImmutable(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "IMMUTABLE"

        @staticproperty
        def string_identifier(self) -> str:
            return "immutable"


    class KInterface(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "INTERFACE"

        @staticproperty
        def string_identifier(self) -> str:
            return "interface"


    class KPrivileged(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "PRIVILEGED"

        @staticproperty
        def string_identifier(self) -> str:
            return "privileged"


    class KFor(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "FOR"

        @staticproperty
        def string_identifier(self) -> str:
            return "for"


    class KStdflush(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "STDFLUSH"

        @staticproperty
        def string_identifier(self) -> str:
            return "stdflush"


    class KReturn(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "RETURN"

        @staticproperty
        def string_identifier(self) -> str:
            return "return"


    class KDo(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "DO"

        @staticproperty
        def string_identifier(self) -> str:
            return "do"


    class KAsync(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "ASYNC"

        @staticproperty
        def string_identifier(self) -> str:
            return "async"


    class KReadonly(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "READONLY"

        @staticproperty
        def string_identifier(self) -> str:
            return "readonly"


    class KImport(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "IMPORT"

        @staticproperty
        def string_identifier(self) -> str:
            return "import"


    class KVal(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "VAL"

        @staticproperty
        def string_identifier(self) -> str:
            return "val"


    class KIn(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "IN"

        @staticproperty
        def string_identifier(self) -> str:
            return "in"


    class KWatch(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "WATCH"

        @staticproperty
        def string_identifier(self) -> str:
            return "watch"


    class KThis(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "THIS"

        @staticproperty
        def string_identifier(self) -> str:
            return "this"


    class KFalse(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "FALSE"

        @staticproperty
        def string_identifier(self) -> str:
            return "false"


    class KAsserteq(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "ASSERTEQ"

        @staticproperty
        def string_identifier(self) -> str:
            return "asserteq"


    class KIntrinsic(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "INTRINSIC"

        @staticproperty
        def string_identifier(self) -> str:
            return "intrinsic"


    class KStdout(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "STDOUT"

        @staticproperty
        def string_identifier(self) -> str:
            return "stdout"


    class KAssertge(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "ASSERTGE"

        @staticproperty
        def string_identifier(self) -> str:
            return "assertge"


    class KProtected(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "PROTECTED"

        @staticproperty
        def string_identifier(self) -> str:
            return "protected"


    class KGoto(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "GOTO"

        @staticproperty
        def string_identifier(self) -> str:
            return "goto"


    class KNew(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "NEW"

        @staticproperty
        def string_identifier(self) -> str:
            return "new"


    class KEnum(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "ENUM"

        @staticproperty
        def string_identifier(self) -> str:
            return "enum"


    class KExtern(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "EXTERN"

        @staticproperty
        def string_identifier(self) -> str:
            return "extern"


    class KRollback(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "ROLLBACK"

        @staticproperty
        def string_identifier(self) -> str:
            return "rollback"


    class KRequire(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "REQUIRE"

        @staticproperty
        def string_identifier(self) -> str:
            return "require"


    class KAssertlt(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "ASSERTLT"

        @staticproperty
        def string_identifier(self) -> str:
            return "assertlt"


    class KConstructor(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "CONSTRUCTOR"

        @staticproperty
        def string_identifier(self) -> str:
            return "constructor"


    class KWhile(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "WHILE"

        @staticproperty
        def string_identifier(self) -> str:
            return "while"


    class KUndefined(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "UNDEFINED"

        @staticproperty
        def string_identifier(self) -> str:
            return "undefined"


    class KElse(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "ELSE"

        @staticproperty
        def string_identifier(self) -> str:
            return "else"


    class KAwait(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "AWAIT"

        @staticproperty
        def string_identifier(self) -> str:
            return "await"


    class KNull(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "NULL"

        @staticproperty
        def string_identifier(self) -> str:
            return "null"


    class KWith(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "WITH"

        @staticproperty
        def string_identifier(self) -> str:
            return "with"


    class KCatch(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "CATCH"

        @staticproperty
        def string_identifier(self) -> str:
            return "catch"


    class KThrow(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "THROW"

        @staticproperty
        def string_identifier(self) -> str:
            return "throw"


    class KFinal(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "FINAL"

        @staticproperty
        def string_identifier(self) -> str:
            return "final"


    class KLet(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "LET"

        @staticproperty
        def string_identifier(self) -> str:
            return "let"


    class KYield(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "YIELD"

        @staticproperty
        def string_identifier(self) -> str:
            return "yield"


    class KAssert(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "ASSERT"

        @staticproperty
        def string_identifier(self) -> str:
            return "assert"


    class KStatic(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "STATIC"

        @staticproperty
        def string_identifier(self) -> str:
            return "static"


    class KNamespace(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "NAMESPACE"

        @staticproperty
        def string_identifier(self) -> str:
            return "namespace"


    class KPublic(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "PUBLIC"

        @staticproperty
        def string_identifier(self) -> str:
            return "public"


    class KVoid(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "VOID"

        @staticproperty
        def string_identifier(self) -> str:
            return "void"


    class KCommit(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "COMMIT"

        @staticproperty
        def string_identifier(self) -> str:
            return "commit"


    class KInstanceof(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "INSTANCEOF"

        @staticproperty
        def string_identifier(self) -> str:
            return "instanceof"


    class KModule(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "MODULE"

        @staticproperty
        def string_identifier(self) -> str:
            return "module"


    class KPrivate(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "PRIVATE"

        @staticproperty
        def string_identifier(self) -> str:
            return "private"


    class KDefault(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "DEFAULT"

        @staticproperty
        def string_identifier(self) -> str:
            return "default"


    class KAtomic(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "ATOMIC"

        @staticproperty
        def string_identifier(self) -> str:
            return "atomic"


    class KBreakpoint(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "BREAKPOINT"

        @staticproperty
        def string_identifier(self) -> str:
            return "breakpoint"


    class KElif(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "ELIF"

        @staticproperty
        def string_identifier(self) -> str:
            return "elif"


    class KConst(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "CONST"

        @staticproperty
        def string_identifier(self) -> str:
            return "const"


    class KMatch(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "MATCH"

        @staticproperty
        def string_identifier(self) -> str:
            return "match"


    class KLambda(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "LAMBDA"

        @staticproperty
        def string_identifier(self) -> str:
            return "lambda"


    class KExtends(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "EXTENDS"

        @staticproperty
        def string_identifier(self) -> str:
            return "extends"


    class KAs(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "AS"

        @staticproperty
        def string_identifier(self) -> str:
            return "as"


    class KFinally(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "FINALLY"

        @staticproperty
        def string_identifier(self) -> str:
            return "finally"


    class KExport(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "EXPORT"

        @staticproperty
        def string_identifier(self) -> str:
            return "export"


    class KTransaction(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "TRANSACTION"

        @staticproperty
        def string_identifier(self) -> str:
            return "transaction"


    class KTypeof(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "TYPEOF"

        @staticproperty
        def string_identifier(self) -> str:
            return "typeof"


    class KAbstract(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "ABSTRACT"

        @staticproperty
        def string_identifier(self) -> str:
            return "abstract"


    class KPackage(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "PACKAGE"

        @staticproperty
        def string_identifier(self) -> str:
            return "package"


    class KTransactional(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "TRANSACTIONAL"

        @staticproperty
        def string_identifier(self) -> str:
            return "transactional"


    class KSynchronized(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "SYNCHRONIZED"

        @staticproperty
        def string_identifier(self) -> str:
            return "synchronized"


    class KCase(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "CASE"

        @staticproperty
        def string_identifier(self) -> str:
            return "case"


    class KFunction(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "FUNCTION"

            self.name: str = ""
            self.arguments: dict = dict()
            self.decorators: list = []

        @staticproperty
        def string_identifier(self) -> str:
            return "function"

        @staticmethod
        def parse(value: list) -> 'Keywords.KFunction':
            fn = Keywords.KFunction()
            value = [x for x in value if x]
            value = value[:-1]
            content = value[-1]
            kwd,name,args = re.match(r"^(function)\s+([a-zA-Z_]+[a-zA-Z0-9_]*)\s*(\(.*)", value[0]).group(1, 2, 3)
            args = [args[1:], *value[1:-1]]

            parsed_args = dict()

            return fn


    class KAssertgt(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "ASSERTGT"

        @staticproperty
        def string_identifier(self) -> str:
            return "assertgt"


    class KOf(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "OF"

        @staticproperty
        def string_identifier(self) -> str:
            return "of"


    class KSwitch(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "SWITCH"

        @staticproperty
        def string_identifier(self) -> str:
            return "switch"


    class KAssertne(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "ASSERTNE"

        @staticproperty
        def string_identifier(self) -> str:
            return "assertne"


    class KMutable(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "MUTABLE"

        @staticproperty
        def string_identifier(self) -> str:
            return "mutable"


    class KImplements(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "IMPLEMENTS"

        @staticproperty
        def string_identifier(self) -> str:
            return "implements"


    class KContinue(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "CONTINUE"

        @staticproperty
        def string_identifier(self) -> str:
            return "continue"


    class KSealed(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "SEALED"

        @staticproperty
        def string_identifier(self) -> str:
            return "sealed"


    class KVar(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "VAR"

        @staticproperty
        def string_identifier(self) -> str:
            return "var"


    class KBreak(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "BREAK"

        @staticproperty
        def string_identifier(self) -> str:
            return "break"


    class KTry(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "TRY"

        @staticproperty
        def string_identifier(self) -> str:
            return "try"


    class KStrictfp(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "STRICTFP"

        @staticproperty
        def string_identifier(self) -> str:
            return "strictfp"


    class KIf(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "IF"

        @staticproperty
        def string_identifier(self) -> str:
            return "if"


    class KSuper(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "SUPER"

        @staticproperty
        def string_identifier(self) -> str:
            return "super"


    class KDefer(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "DEFER"

        @staticproperty
        def string_identifier(self) -> str:
            return "defer"


    class KTrue(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "TRUE"

        @staticproperty
        def string_identifier(self) -> str:
            return "true"


    class KDelete(Keyword):
        def __init__(self):
            super().__init__();
            self.token_name = "DELETE"

        @staticproperty
        def string_identifier(self) -> str:
            return "delete"

ReservedKeywords = {"with", "assert", "readonly", "false", "throw", "strictfp", "in", "intrinsic", "module", "typeof", "elif", "breakpoint", "switch", "from", "return", "extern", "super", "assertNe", "continue", "assertLe", "else", "assertGe", "this", "private", "catch", "do", "abstract", "if", "transactional", "function", "immutable", "protected", "case", "synchronized", "void", "implements", "yield", "try", "of", "static", "undefined", "commit", "mutable", "instanceof", "export", "await", "constructor", "const", "assertGt", "public", "package", "match", "transaction", "defer", "async", "import", "extends", "assertLt", "null", "goto", "true", "default", "volatile", "rollback", "val", "let", "sealed", "assertEq", "enum", "as", "for", "final", "while", "interface", "watch", "break", "class", "finally", "delete", "namespace", "var", "require", "new", "atomic", "lambda", "privileged", "stdout", "stdflush", "global"}

def MatchKeyword(keyword: str) -> Keyword:
    match keyword:
        case "instanceof": return Keywords.KInstanceof
        case "final": return Keywords.KFinal
        case "of": return Keywords.KOf
        case "match": return Keywords.KMatch
        case "breakpoint": return Keywords.KBreakpoint
        case "interface": return Keywords.KInterface  
        case "namespace": return Keywords.KNamespace  
        case "var": return Keywords.KVar
        case "new": return Keywords.KNew
        case "null": return Keywords.KNull
        case "require": return Keywords.KRequire
        case "private": return Keywords.KPrivate
        case "from": return Keywords.KFrom
        case "assertle": return Keywords.KAssertle
        case "assertge": return Keywords.KAssertge
        case "await": return Keywords.KAwait
        case "default": return Keywords.KDefault
        case "with": return Keywords.KWith
        case "assertgt": return Keywords.KAssertgt
        case "class": return Keywords.KClass
        case "transactional": return Keywords.KTransactional
        case "volatile": return Keywords.KVolatile
        case "package": return Keywords.KPackage
        case "constructor": return Keywords.KConstructor
        case "val": return Keywords.KVal
        case "finally": return Keywords.KFinally
        case "as": return Keywords.KAs
        case "false": return Keywords.KFalse
        case "super": return Keywords.KSuper
        case "rollback": return Keywords.KRollback
        case "stdflush": return Keywords.KStdflush
        case "yield": return Keywords.KYield
        case "extends": return Keywords.KExtends
        case "break": return Keywords.KBreak
        case "catch": return Keywords.KCatch
        case "case": return Keywords.KCase
        case "undefined": return Keywords.KUndefined
        case "assertne": return Keywords.KAssertne
        case "if": return Keywords.KIf
        case "for": return Keywords.KFor
        case "stdout": return Keywords.KStdout
        case "commit": return Keywords.KCommit
        case "implements": return Keywords.KImplements
        case "protected": return Keywords.KProtected
        case "elif": return Keywords.KElif
        case "void": return Keywords.KVoid
        case "mutable": return Keywords.KMutable
        case "readonly": return Keywords.KReadonly
        case "do": return Keywords.KDo
        case "defer": return Keywords.KDefer
        case "let": return Keywords.KLet
        case "import": return Keywords.KImport
        case "async": return Keywords.KAsync
        case "export": return Keywords.KExport
        case "extern": return Keywords.KExtern
        case "public": return Keywords.KPublic
        case "atomic": return Keywords.KAtomic
        case "goto": return Keywords.KGoto
        case "lambda": return Keywords.KLambda
        case "assert": return Keywords.KAssert
        case "return": return Keywords.KReturn
        case "synchronized": return Keywords.KSynchronized
        case "immutable": return Keywords.KImmutable
        case "continue": return Keywords.KContinue
        case "try": return Keywords.KTry
        case "enum": return Keywords.KEnum
        case "else": return Keywords.KElse
        case "assertlt": return Keywords.KAssertlt
        case "typeof": return Keywords.KTypeof
        case "static": return Keywords.KStatic
        case "while": return Keywords.KWhile
        case "throw": return Keywords.KThrow
        case "intrinsic": return Keywords.KIntrinsic
        case "module": return Keywords.KModule
        case "privileged": return Keywords.KPrivileged
        case "delete": return Keywords.KDelete
        case "switch": return Keywords.KSwitch
        case "watch": return Keywords.KWatch
        case "strictfp": return Keywords.KStrictfp
        case "abstract": return Keywords.KAbstract
        case "transaction": return Keywords.KTransaction
        case "in": return Keywords.KIn
        case "sealed": return Keywords.KSealed
        case "asserteq": return Keywords.KAsserteq
        case "function": return Keywords.KFunction
        case "this": return Keywords.KThis
        case "const": return Keywords.KConst
        case "true": return Keywords.KTrue
        case "global": return Keywords.KGlobal