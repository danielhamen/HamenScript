def split_code(code: str) -> str:
    is_str = False
    code_lines = [""]
    for i,char in enumerate(code):
        if char == "\"" and code[i-1] != "\\":
            is_str = not is_str
        elif char == "\n":
            continue
        elif not is_str:
            pass

        code_lines[-1] += char