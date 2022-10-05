import re as regex


class Token:
    """
    A `Token` represents a single unit of code. 
    """

    type: str
    """
    The type of token, such as `keyword` or `class name`. Certain types may only exist in certain languages, such as `preprocessor directive` for `C++`.
    """

    value: str
    """
    The part of the token's match that represents the actual value of the token, such as `public` for a `keyword` token. This differs from `full_match` in that some token types have to check characters around the token to correctly identify it, and those characters are not included in the value of the token itself.
    """

    full_match: str
    """
    The entire match of the token's regular expression. The exact definition of this varies from implementation to implementation, but in general it refers to the `0` group of the regular expression used to identify the token. 
    """

    start: int
    """The index of the entire code block at which the first letter of this token lies."""

    end: int
    """The index of the entire code block at which the last letter of this token lies. """

    def __init__(self, type: str, value: str, full_match: regex.Match, start: int, end: int):
        """
        Creates a new `Token`. 

        ### Parameters
            - `type: str`:
                - The type of token, such as `keyword` or `class name`.
            - `value: str`:
                - The value of the token, such as `public`. 
            - `full_match: re.Match`
                - The full group matched by the token's regular expression.
            - `start: int`
                - The index of the first character of this token relative to the entire code snippet.
            - `end: int`
                - The index of the last character of this token relative to the entire code snippet. 
        
        ### Returns
        a new `Token` with the specified attributes.

        """
        self.type = type
        self.value = value
        self.full_match = full_match
        self.start = start
        self.end = end

    def __str__(self):
        return f"Token[ type = {self.type}, value = {self.value}, start = {self.start}, end = {self.end} ]"


class TokenIdentifier:

    regex: str
    group: int
    type: str

    def __init__(self, token_type, regex, group = 0, has_sub_tokens = False):
        self.regex = regex if regex.startswith("^") else f"^{regex}"
        self.type = token_type
        self.group = group
        

class TokenizableLanguage:

    identifiers: list[TokenIdentifier]
    default_identifiers = [
        TokenIdentifier("left parentheses", r"^\("),
        TokenIdentifier("right parentheses", r"^\)"),
        TokenIdentifier("left brace", r"^\{"),
        TokenIdentifier("right brace", r"^\}"),
        TokenIdentifier("semicolon", r"^;"),
        TokenIdentifier("left bracket", r"^\["),
        TokenIdentifier("right bracket", r"^\]"),
        TokenIdentifier("dot", r"^\."),
        TokenIdentifier("colon", r"^:"),
        TokenIdentifier("number", r"^-?\d+(\.\d+)?"),
        TokenIdentifier("operation", r"^(=(==?)?\+|-|\*|/|%|&&?|\|\|?|!)", 1),
        TokenIdentifier("string", r'^"([^"]|\\")*"'),
        TokenIdentifier("constant", r"^[A-Z_]+\b"),
        TokenIdentifier("class name", r"^[A-Z](\w)*\b"),
        TokenIdentifier("function", r"^([A-Za-z_]\w*)\s*\(", 1),
        TokenIdentifier("identifier", r"^[a-z_]\w*\b"),
        TokenIdentifier("whitespace", r"^\s+"),
        TokenIdentifier("newline", r"^\n+"),
        TokenIdentifier("comment", r"^//[^\n]*"),
        TokenIdentifier("star", r"^\*"),
        TokenIdentifier("spread", "...")
    ]

    def __init__(self, identifiers: list[TokenIdentifier]):
        """
        Creates a new programming language that can be tokenized. By default, several `TokenIdentifiers` are in place that are common in many languages, such as matching `r"^//[^\\n]*"` for `comment`. Any identifier passed to the `identifiers` parameter with the same name as a default `TokenIdentifier` will override the default in place, such as:

        ```python
        Python = TokenizableLanguage(
            identifiers = [
                TokenIdentifier("comment", r"#[^\\n]*"),
                ...
            ]
        )
        ```

        For a full comprehensive list of default token identifiers, see `default_identifiers`.
        """

        # Empty dictionary
        id_dict = {}

        # Add default identifiers 
        for default_identifier in TokenizableLanguage.default_identifiers:
            id_dict[default_identifier.type] = default_identifier

        # Add and override identifier arguments
        for identifier in identifiers:
            id_dict[identifier.type] = identifier

        # Reverse identifier dictionary so that arguments come first (and thus their regexs have priority)
        self.identifiers = list(id_dict.values()).reverse()
                    

    def tokenize(self, code) -> list[Token]:
        """
        Tokenizes the given code snippet into a `list` of `Tokens` using this `TokenizableLanguage`.
        """
        tokens = []
        pos = 0
        while(code):
            match_found = False
            while(code.startswith("\n")):
                code = code[1:]
            for identifier in self.identifiers + TokenizableLanguage.default_identifiers:
                match = regex.match(identifier.regex, code)
                if (match):
                    str_match = match.group(identifier.group)
                    token = Token(
                        type = identifier.type, 
                        value = match.group(identifier.group),
                        full_match = match,
                        start = pos,
                        end = pos + len(str_match)
                    )
                    code = code[len(str_match):]
                    pos += len(str_match)
                    tokens.append(token)
                    match_found = True
                    break
            if not match_found: raise Exception("No match found: " + code)
        return tokens


# Assembly

C = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while)\b"),
    ]
)
"""
The `C` programming language, instantiated as a `TokenizableLanguage`.

### Keyword recognition
All of the following, and no others, are recognized as reserved keywords in the `C` language:

`auto`, `break`, `case`, `char`, `const`, `continue`, `default`, `do`, `double`, `else`, `enum`, `extern`, `float`, `for`, `goto`, `if`, `int`, `long`, `register`, `return`, `short`, `signed`, `sizeof`, `static`, `struct`, `switch`, `typedef`, `union`, `unsigned`, `void`, `volatile`, and `while`.

### Comment recognition
Comments are interpreted as a double forward slash (`//`) followed by all non-newline characters. 

### Identifier recognition
A valid `C` identifier is recognized as a letter followed by either a letter, digit, or underscore, zero or more times. 

### Class recognition
A class name is recognized as a valid identifier that begins with a capital letter.

### Function recognition
A function is recognied by any valid identifier, followed by zero or more whitespace, followed by a left parentheses. The parentheses will not be included in the token's value.

### String recognition
A string is recognied as an opening double quotes (`"`), followed by any character that is either a non-double quote character or an escaped double quote (`\\"`) zero or more times, followed by a closing double quotes (`"`).

### Constant recognition
A constant is recognized as a valid identifier that only contains capital letters and underscores.
"""

Cpp = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(alignas|alignof|and|and_eq|asm|atomic|cancel|atomic|commit|atomic|noexcept|auto|bitand|bitor|bool|break|case|catch|char|char8_t|char16_t|char32_t|class|compl|concept|const|consteval|constexpr|constinit|const_cast|continue|co_await|co_return|co_yield|decltype|default|delete|do|double|dynaimc_cast|else|enum|explicit|export|extern|float|for|friend|goto|if|inline|int|long|mutable|namespace|new|noexcept|not|not_eq|nullptr|operator|or|or_eq|private|protected|public|reflexpr|register|reinterpret_cast|requires|return|short|signed|sizeof|static|static_assert|static_cast|struct|switch|synchronized|template|thread_local|throw|try|typedef|typeid|typename|union|unsigned|using|virtual|void|volatile|wchar_t|while|xor|xor_eq)\b"),
        TokenIdentifier("keyword literal", r"(false|nullptr|this|true)\b")
    ]
)

CSharp = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(abstract|as|base|bool|break|byte|case|catch|char|checked|class|const|continue|decimal|default|delegate|do|double|else|enum|event|explicit|extern|finally|fixed|float|for|foreach|goto|if|implicit|in|int|interface|internal|is|lock|long|namespace|new|object|operator|out|override|params|private|protected|public|readonly|ref|return|sbyte|sealed|short|sizeof|stackalloc|static|string|struct|switch|throw|try|typeof|uint|ulong|unchecked|unsafe|ushort|using|using|static|void|volatile|while)\b"),
        TokenIdentifier("keyword literal", r"(false|null|this|true)\b")
    ]
)

Go = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(break|case|chan|const|continue|default|defer|else|fallthrough|for|func|go|goto|if|import|interface|map|package|range|return|select|struct|switch|type|var)\b"),
    ]
)

Haskell = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(case|class|data|default|deriving|do|else|forall|if|import|in|infix|infixl|infixr|instance|let|module|newtype|of|qualified|then|type|where|_|foreign|ccall|as|safe|unsafe`)\b")
    ]
)

Java = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(abstract|assert|boolean|break|byte|case|catch|char|class|continue|default|do|double|else|enum|extends|final|finally|float|for|if|implements|import|instanceof|int|interface|long|native|new|package|public|return|short|static|strictfp|super|switch|synchronized|throw|throws|transient|try|void|volative|while)\b", 1),
        TokenIdentifier("keyword literal", r"(false|null|this|true)\b")
    ]
)

JavaScript = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(as|break|case|catch|class|const|constructor|continue|debugger|default|delete|do|else|enum|export|extends|finally|for|from|function|get|if|import|in|instanceof|new|let|module|of|return|set|super|static|string|switch|throw|try|var|while|with|yield)\b"),
        TokenIdentifier("keyword literal", r"(false|null|this|true)\b")
    ]
)

Lua = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(and|break|do|else|elseif|end|false|for|function|if|in|local|not|or|repeat|return|then|true|until|while)\b"),
        TokenIdentifier("keyword literal", r"(nil)\b")
    ]
)

Python = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(and|as|assert|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b"),
        TokenIdentifier("keyword literal", r"(False|None|self|True)\b"),
        TokenIdentifier("comment", r"#[^\n]*"),
    ]
)

Ruby = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(__ENCODING__|__LINE|__FILE__|BEGIN|END|alias|and|begin|break|case|class|def|defined|do|else|elsif|end|ensure|for|if|in|module|next|not|or|redo|rescue|retry|return|super|then|trueundef|unless|until|when|while|yield)\b"),
        TokenIdentifier("keyword literal", r"(false|nil|self|true)\b")
    ]
)

Rust = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(as|async|await|break|consts|continue|crate|dyn|else|enum|extern|fn|for|if|impl|in|let|loop|match|mod|move|mut|pub|ref|return|Self|static|struct|super|trait|type|unsafe|use|where|while)\b"),
        TokenIdentifier("keyword literal", r"(false|self|true)\b")
    ],
)

SQL = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(ADD|ALL|ALTER|AND|ANY|AS|ASC|BACKUP|BETWEEN|CASE|CHECK|COLUMN|CONSTRAINT|CREATE|DATABASE|INDEX|OR|REPLACE|VIEW|TABLE|PROCEDURE|UNIQUE|INDEX|DEFAULT|DELETE|DESC|DISTINCT|DROP|EXEC|EXISTS|FOREIGN|KEY|FROM|FULL|OUTER|JOIN|GROUP|BY|HAVING|IN|INNER|JOIN|INSERT|INTO|SELECT|IS|NULL|NOT|LEFT|LIKE|LIMIT|NOT|OR|ORDER|OUTER|PRIMARY|PROCEDURE|RIGHT|ROWNUM|INTO|TOP|SET|TABLE|TOP|TRUNCATE|UNION|ALL|UPDATE|VALUES|WHERE)\b")
    ]
)

TypeScript = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(any|as|boolean|break|case|catch|class|const|constructor|continue|debugger|declare|default|delete|do|else|enum|export|extends|finally|for|from|function|get|if|implements|import|in|instanceof|interface|new|let|module|number|of|private|protected|public|require|return|set|super|static|string|switch|symbol|throw|try|type|typeof|var|void|while|with|yield)\b"),
        TokenIdentifier("keyword literal", r"(false|null|this|true)\b")
    ]
)

# XML