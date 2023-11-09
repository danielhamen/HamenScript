from hs.Globals import resetGlobals

def END_CODE(code: int = None) -> None:
    resetGlobals()

    exit("\n\n--- HAMENSCRIPT END" + (f"( {code} )" if code else "") + " ---")

def START_CODE(flags: str = None) -> None:
    resetGlobals()

    print(f"--- HAMENSCRIPT START " + (f"~ {flags.upper()}" if flags else "") + " ---\n")