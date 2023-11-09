import shutil
import os
import subprocess
import sys
from enum import Enum

from hs.lib.staticproperty import staticproperty
from hs.lib.ErrorReferences import ErrorReferences

class Symbols:
    class Types:
        """
        Primitive (built-in) types
        """

        from hs.lib.Symbols.Types import Primitive,Number,String,Boolean

    class Tokens:
        """
        Various tokens
        """

        from hs.lib.Symbols.Tokens import (Token)
        from hs.lib.Symbols.Keywords import (Keywords,Keyword,ReservedKeywords,MatchKeyword)
        from hs.lib.Symbols.Variable import Variable
        from hs.lib.Symbols.Decorator import Decorator

    class Operators:
        from hs.lib.Symbols.Operator import (Operator,Classifications)

class System:
    class Standard:
        class out:
            class println:
                def __init__(self, *message, sep: str = " "):
                    sys.stdout.write(sep.join([message]) + "\n")
                    sys.stdout.flush()

            class print:
                def __init__(self, *message, sep: str = " "):
                    sys.stdout.write(sep.join([message]))

            class flush:
                def __init__(self):
                    sys.stdout.flush()

            class clear:
                def __init__(self):
                    os.system("clear")

    class OS:
        class execute:
            def __init__(self, command: str, *, show_output: bool = False):
                self.command = command
                self.output = subprocess.check_output(command, shell = show_output, text = True)

        class Environment:
            @staticmethod
            def get_variable(variable: str) -> str | None:
                return os.environ.get(variable)

            @staticmethod
            def set_variable(variable: str, value):
                os.environ[variable] = value

            @staticmethod
            def get_variables() -> dict:
                return dict(os.environ.items())

        class File:
            @staticmethod
            def listdir(directory: str, *, files: bool = True, directories: bool = True) -> list[str]:
                return [x for x in os.listdir(directories) if (os.path.isdir(x) and directories) or (os.path.isfile(x) and files)]

            class remove:
                @staticmethod
                def dir(directory: str) -> None:
                    shutil.rmtree(directory, True)

                @staticmethod
                def file(file: str) -> None:
                    os.remove(file)

            class create:
                @staticmethod
                def dir(directory: str) -> None:
                    os.mkdir(directory)

                @staticmethod
                def file(file: str) -> None:
                    open(file, "x").close()

from hs.lib.Common import Common

class ExecutionControl:
    from hs.lib.ExecutionControl import END_CODE,START_CODE