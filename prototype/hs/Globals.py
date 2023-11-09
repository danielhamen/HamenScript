import os
import json

__GLOBALS__ = os.path.join(os.path.dirname(__file__), "Globals.json")

default = {
    "__TAB_SIZE__": 4,
    "__TAB_BASE__": " ",
    "__ML_COMMENTS__": r"\/\*[\s\S]*?\*\/",
    "__SL_COMMENTS__": r"\/\/.*",
}

def getGlobals() -> dict:
    with open(__GLOBALS__, "r") as f:
        data = json.load(f)
        assert data

        return data

def resetGlobal(key: str):
    assert key in default

    setGlobal(key, default[key])

def resetGlobals():
    with open(__GLOBALS__, "w") as f:
        json.dump(default, f)

def getGlobal(key: str):
    if key not in default: return False

    return getGlobals()[key]

def setGlobal(key: str, value: int | float | bool | str | list[int | float | bool | str]):
    if key not in default: return False

    _globals = default.copy()
    _globals[key] = value.real

    with open(__GLOBALS__, "w") as f:
        json.dump(_globals, f)