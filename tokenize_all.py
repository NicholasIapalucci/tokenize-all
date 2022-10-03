import re as regex


class Token:

    type: str
    value: str
    start: int
    end: int

    def __init__(self, type: str, value: str, start: int, end: int):
        self.type = type
        self.value = value
        self.start = start
        self.end = end

    def __str__(self):
        return f"Token[ type = {self.type}, value = {self.value}, start = {self.start}, end = {self.end} ]"


class TokenIdentifier:

    regex: str
    group: int
    type: str
    start: int
    end: int

    def __init__(self, token_type, regex, group = 0):
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
        TokenIdentifier("number", r"-?\d+(\.\d+)?"),
        TokenIdentifier("operation", r"(=(==?)?\+|-|\*|/|%|&&?|\|\|?|!)", 1),
        TokenIdentifier("string", r'"([^"]|\\")*"'),
        TokenIdentifier("constant", r"[A-Z]+\b"),
        TokenIdentifier("class name", r"[A-Z](\w)*\b"),
        TokenIdentifier("function", r"([A-Za-z_]\w*)\s*\(", 1),
        TokenIdentifier("identifier", r"[a-z_]\w*\b"),
    ]

    def __init__(self, identifiers: list[TokenIdentifier]):
        self.identifiers = identifiers

    def tokenize(self, code) -> list[Token]:
        tokens = []
        pos = 0
        while(code):
            match_found = False
            while(code.startswith("\n")):
                code = code[1:]
            for identifier in self.identifiers + TokenizableLanguage.default_identifiers:
                match = regex.match(r"^\s+", code)
                if (match):
                    code = code[len(match.group()):]
                    pos += len(match.group())
                    match_found = True
                    break
                match = regex.match(identifier.regex, code)
                if (match):
                    str_match = match.group(identifier.group)
                    token = Token(
                        type = identifier.type, 
                        value = match.group(identifier.group),
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


C = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while)\b"),
        TokenIdentifier("comment", r"//[^\n]*"),
    ]
)

Cpp = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(alignas|alignof|and|and_eq|asm|atomic|cancel|atomic|commit|atomic|noexcept|auto|bitand|bitor|bool|break|case|catch|char|char8_t|char16_t|char32_t|class|compl|concept|const|consteval|constexpr|constinit|const_cast|continue|co_await|co_return|co_yield|decltype|default|delete|do|double|dynaimc_cast|else|enum|explicit|export|extern|false|float|for|friend|goto|if|inline|int|long|mutable|namespace|new|noexcept|not|not_eq|nullptr|operator|or|or_eq|private|protected|public|reflexpr|register|reinterpret_cast|requires|return|short|signed|sizeof|static|static_assert|static_cast|struct|switch|synchronized|template|this|thread_local|throw|true|try|typedef|typeid|typename|union|unsigned|using|virtual|void|volatile|wchar_t|while|xor|xor_eq)\b"),

    ]
)

Java = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(abstract|assert|boolean|break|byte|case|catch|char|class|continue|default|do|double|else|enum|extends|final|finally|float|for|if|implements|import|instanceof|int|interface|long|native|new|null|package|public|return|short|static|strictfp|super|switch|synchronized|this|throw|throws|transient|try|void|volative|while)\b", 1),
        TokenIdentifier("comment", r"//[^\n]*")
    ]
)

Python = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(and|as|assert|break|class|continue|def|del|elif|else|except|False|finally|for|from|global|if|import|in|is|lambda|None|nonlocal|not|or|pass|raise|return|True|try|while|with|yield)\b"),
        TokenIdentifier("comment", r"#[^\n]*"),
    ]
)

TypeScript = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(any|as|boolean|break|case|catch|class|const|constructor|continue|debugger|declare|default|delete|do|else|enum|export|extends|false|finally|for|from|function|get|if|implements|import|in|instanceof|interface|new|let|module|null|number|of|package|private|protected|public|require|return|set|super|static|string|switch|symbol|this|throw|true|try|type|typeof|var|void|while|with|yield)\b"),
        TokenIdentifier("comment", r"//[^\n]*")
    ]
)