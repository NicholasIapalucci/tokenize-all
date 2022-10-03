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
        TokenIdentifier("dot", r"^\.")
    ]

    def __init__(self, identifiers: list[TokenIdentifier]):
        self.identifiers = identifiers

    def tokenize(self, code) -> list[Token]:
        tokens = []
        code = regex.sub("\n", " ", code)
        pos = 0
        while(code):
            for identifier in TokenizableLanguage.default_identifiers + self.identifiers:
                match = regex.match(r"\s+", code)
                if (match):
                    code = code[len(match.group()):]
                    pos += len(match.group())
                    continue
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
        return tokens


Java = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(abstract|assert|boolean|break|byte|case|catch|char|class|continue|default|do|double|else|enum|extends|final|finally|float|for|if|implements|import|instanceof|int|interface|long|native|new|null|package|public|return|short|static|strictfp|super|switch|synchronized|this|throw|throws|transient|try|void|volative|while)\b", 1),
        TokenIdentifier("string", r'"([^"]|\\")*"'),
        TokenIdentifier("number", r"-?\d+(\.\d+)?"),
        TokenIdentifier("operation", r"(=|==|\+|-|\*|/|%|&&|\|\||!)", 1),
        TokenIdentifier("constant", r"[A-Z]+\b"),
        TokenIdentifier("class name", r"[A-Z](\w)*\b"),
        TokenIdentifier("function", r"([A-Za-z_]\w*)\s*\(", 1),
        TokenIdentifier("identifier", r"[A-Za-z_]\w*\b"),
    ]
)

tokens = Java.tokenize(
"""
public class Main {

    public static void main(String[] args) {
        System.out.println("hello world");
    }
}
"""
)

for token in tokens: print(token)