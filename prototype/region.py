import math

name = "[ HamenScript Symbol Value Encoding ]"
width = 80
if len(name) % 2 != 0:
    width += 1

whitespace = width - len(name) - 3 - 3
whitespace //= 2

print("\n".join([
    "#" * width,
    "###" + (" " * (width - 6)) + "###",
    "###" + (" " * whitespace) + name + (" " * whitespace) + "###",
    "###" + (" " * (width - 6)) + "###",
    "#" * width
]))