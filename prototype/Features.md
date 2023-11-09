# HamenScript

## Introduction

HamenScript is a general-purpose high-level programming language

## Features:

HamenScript has many highly-unique features. Many of which is not in popular languages like Java, Python, C++, etc, making HamenScript a wise-choice for your workflow

In addition, it is imperative to understand and learn all of its features, as when HamenScript and its unique features are correctly and fully used, you can effectively create incredibly-efficient, optimized, and versatile programs ranging from command-line interfaces, to a GUI-based software, to even web applications using HamenScript as not only your back-end framework, but also your front-end!

Note that this documentation is not in any order of difficulty. Features are not rated to be from easiest-to-smallest so we recommend using this as a reference, and not a guide.

### `#PRAGMA` notation

With pragma notation, you can define settings before the interpreter has started. Though pragma notation can be passed via command-line-parameters, this section refers to in-code pragma notation&mdash;the term "Pragma Notation" refers to in-code pragma-declarations, whereas the term "CLI Pragma Parameters" or "Pragma Parameter Passing" *generally* refers to the passing of these parameters in the cli.

Pragma notation occurs at the top of a `Main.hs` file&mdash;note that it must be declared inside `Main.hs` as this is the root of your package; sub-files will automatically inherit pragma declarations defined in the root package file, `Main.hs`

Pragma notation has the following syntax:

`#PRAGMA :: <KEY> >> <VALUE>;`

Where:
- `KEY`: a pragma-key; a list of all keys can be found at [Pragma Key List](#prgma-keys) and are normally in the format of: `^__[a-zA-Z_]*__$`, though this construct is not encored nor always adhered
- `VALUE`: a pragma-value; either a string, number, or boolean is supported&mdash;these types are *not* denoted in any special way. Additionally, this value must match the default data-type of the key&mdash;that is, you cannot pass `false` to the `__TAB_SIZE__` pragma key as it only accepts numbers

Note that pragma notation is extremely strict; failure to comply with any syntactic or semantic rules will result in an error

Finally, it is notable that protected pragma keys (pragma keys with the "X" prefix&mdash;e.g. *\_\_XKEY\_\_*) are not accessible via pragma notation as they should only be modified in the interpreter-context