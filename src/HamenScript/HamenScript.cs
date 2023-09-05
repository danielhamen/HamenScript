using System;
using System.Collections.Generic;

class ITokens
{
    class Function
    {
        private string code;

        Function()
        {
            this.code = "";
        }

        void Parse(string code)
        {
            this.code = code;
        }
    }
}

class ICommon
{
    public List<string> SplitCode(string code)
    {
        List<string> codeLines = new List<string>();
        codeLines.Add("");

        int level = 0;
        bool isString = false;
        for (int i = 0; i < code.Length; i++) {
            char _char = code[i];

            if (_char == '{' && !isString) {
                level += 1;
            } else if (_char == '}' && !isString) {
                level -= 1;
            } else if (_char == '`' && code[i-1] != '\\') {
                isString = !isString;
            };

            if (level != 0) {
                codeLines[codeLines.Count - 1] += _char;
            } else if (level == 0 && !isString && _char == ';') {
                codeLines.Add("");
            } else {
                codeLines[codeLines.Count - 1] += _char;
            }
        };

        return codeLines;
    }
}

class Globals
{
    private List<string> globals;
    Globals()
    {
        this.globals.Add("");
    }

    public void Add(string glob)
    {
        this.globals.Add(glob);
    }
}

class Interpret
{
    public string code;

    Interpret(string code)
    {
        this.code = code;
    }
}

namespace HamenScript
{

    class Program
    {
        static void Main(string[] args)
        {
            ICommon Common = new ICommon();
            ITokens Tokens = new ITokens();

            string code = "const x: Number = 13;let y: Number = 22;";

            List<string> codeLines = Common.SplitCode(code);

            foreach (string line in codeLines)
            {
                Console.WriteLine(line);
            }
        }
    }
}