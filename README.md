# Tokenize-All

Tokenize blocks of code in Python. Used by `manim-code-blocks` to syntax highlight blocks of code. 

## Example Usage

```python
from tokenize_all import Java

tokens = Java.tokenize(
    """
    public class Main {
        public static void main(String[] args) {
            System.out.println("Hello world!");
        }
    }
    """
)

for token in tokens: print(token)
```

Output:

```
>> Token[ type = keyword, value = public, start = 4, end = 10 ]
>> Token[ type = keyword, value = class, start = 11, end = 16 ]
>> Token[ type = class name, value = Main, start = 17, end = 21 ]
>> Token[ type = left brace, value = {, start = 22, end = 23 ]
>> Token[ type = keyword, value = public, start = 31, end = 37 ]
>> Token[ type = keyword, value = static, start = 38, end = 44 ]
>> Token[ type = keyword, value = void, start = 45, end = 49 ]
>> Token[ type = function, value = main, start = 50, end = 54 ]
>> Token[ type = left parentheses, value = (, start = 54, end = >> 55 ]
>> Token[ type = class name, value = String, start = 55, end = >> 61 ]
>> Token[ type = left bracket, value = [, start = 61, end = 62 ]
>> Token[ type = right bracket, value = ], start = 62, end = 63 ]
>> Token[ type = identifier, value = args, start = 64, end = 68 ]
>> Token[ type = right parentheses, value = ), start = 68, end = >> 69 ]
>> Token[ type = left brace, value = {, start = 70, end = 71 ]
>> Token[ type = class name, value = System, start = 83, end = >> 89 ]
>> Token[ type = dot, value = ., start = 89, end = 90 ]
>> Token[ type = identifier, value = out, start = 90, end = 93 ]
>> Token[ type = dot, value = ., start = 93, end = 94 ]
>> Token[ type = function, value = println, start = 94, end = >> 101 ]
>> Token[ type = left parentheses, value = (, start = 101, end = >> 102 ]
>> Token[ type = string, value = "Hello world!", start = 102, >> end = 116 ]
>> Token[ type = right parentheses, value = ), start = 116, end >> = 117 ]
>> Token[ type = semicolon, value = ;, start = 117, end = 118 ]
>> Token[ type = right brace, value = }, start = 126, end = 127 ]
>> Token[ type = right brace, value = }, start = 131, end = 132 ]
```