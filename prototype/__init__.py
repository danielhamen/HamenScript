import Common

class InterpretDeclarative:
    def __init__(self, code: list or str):
        self.code = code
        if type(self.code) is str:
            self.code = Common.split_code(self.code)

if __name__ == "__main__":
    with open(r"prototype\test.hds", "r") as code:
        InterpretDeclarative(code.read())