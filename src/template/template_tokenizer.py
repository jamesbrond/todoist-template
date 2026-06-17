"""Tokenize template"""
from pathlib import Path
import re
import logging
from enum import Enum
from abc import ABC, abstractmethod


TokenType = Enum('TokenType', ['TEMPLATE', 'PLAINTEXT', 'PLACEHOLDER'])


# Include pattern: optional leading spaces + #! include <filename>
RE_INCLUDES = re.compile(r"(.*)#!\s*include +([A-Za-z0-9\/._-]+)")
# Variable pattern: {var_name|default_value}
RE_VARS = re.compile(r"{(\w+)\s*\|?\s*([^}]+)?}")
# Comments patterns: lines starting with # (not #!) and inline comments
RE_COMMENTS = re.compile(r"(?m)^ *#[^!].*[\n\r]?", re.MULTILINE)
# Inline comments pattern: # followed by anything except !
RE_INLINE_COMMENTS = re.compile(r"\s*#+(?!!).*")
# Empty lines pattern
RE_EMPTY_LINE = re.compile(r"^\s*$\r?\n", re.MULTILINE)


def get_template(text: str = None, file: Path | None = None) -> tuple[str, Path]:
    """Get template source and folder"""

    if text is not None:
        return text, Path(__file__).resolve().absolute().parent

    if file is not None and file.exists():
        return file.read_text(encoding="utf-8"), file.resolve().absolute().parent

    raise ValueError("Text or filename must be provided")


def purge_comments(text: str) -> str:
    """Remove all comments from template text; both full-line and inline comments"""
    txt = text
    txt = re.sub(RE_COMMENTS, '', txt)
    txt = re.sub(RE_INLINE_COMMENTS, '', txt)
    txt = re.sub(RE_EMPTY_LINE, '', txt)
    return txt


def includes(text: str):
    """Yield all include matches in the text"""
    yield from RE_INCLUDES.finditer(text)


def preprocessing_includes(text: str) -> list:
    """Preprocess include statements"""
    return list(includes(text))


def tokenize(text: str):
    """Yield all variable matches in the text"""
    yield from RE_VARS.finditer(text)


def preprocessing(text: str) -> list:
    """Preprocess variable tokens"""
    return list(tokenize(text))


class AbstractTemplateToken(ABC):
    """Abstract template token"""

    def __init__(self, text: str, token_type: TokenType) -> None:
        self._source = text
        self._token_type = token_type

    @abstractmethod
    def render(self, variables: dict) -> str:
        """Render token"""

    def raw(self) -> str:
        """Return template not processed"""
        return self._source

    def __repr__(self) -> str:
        return f"Token[{self._token_type.name}]({self._source})"


class PlainTextToken(AbstractTemplateToken):
    """
    Simple plain text token

    Example:
        Hello, this is a plain text.
    """
    def __init__(self, text: str):
        super().__init__(text, TokenType.PLAINTEXT)

    def render(self, variables: dict) -> str:
        # return plain text as is
        return self._source


class PlaceholderToken(AbstractTemplateToken):
    """
    Token with placeholder variable

    Examples:
        {username|Guest}
        {due_date}
    """
    def __init__(self, text):
        super().__init__(text, TokenType.PLACEHOLDER)
        match = RE_VARS.search(text)
        self._var_name, self._default_value = match.group(1), match.group(2)

    def render(self, variables: dict) -> str:
        return variables.get(self._var_name) if self._var_name in variables else self._default_value or self._source


class TemplateToken(AbstractTemplateToken):
    """
    Parse a template file or string and tokenize it

    Example:
        Hello, {username|Guest}!
        #! include footer.txt
    """
    def __init__(self,  # pylint: disable=too-many-positional-arguments
                 text: str = None,
                 file: Path = None,
                 line_prefix: str = "",
                 keep_comments: bool = False):
        super().__init__("", TokenType.TEMPLATE)

        self._filepath = file
        self._line_prefix = line_prefix
        self._keep_comments = keep_comments

        self._source, folder = get_template(text=text, file=file)

        text = self._source if self._keep_comments else purge_comments(self._source)

        self._tokens = self._compile(text, folder)

    def render(self, variables: dict) -> str:
        """Render template tokens as a single output string"""
        out = ''
        for token in self._tokens:
            out += token.render(variables)

        padding = len(self._line_prefix)
        if padding > 0:
            lines = out.splitlines()
            out = f"{self._line_prefix}{lines[0]}\n"
            # add padding to all lines but the first one
            out += "\n".join([f"{' ' * padding}{x}" for x in lines[1:]])
        logging.debug("%s\n%s", self._filepath.name if hasattr(self._filepath, "name") else self._filepath, out)
        return out

    def _compile(self, text: str, folder: Path) -> list[AbstractTemplateToken]:
        # parse template source and generate an object ready to be rendered
        matches = [*preprocessing_includes(text), *preprocessing(text)]
        matches.sort(key=lambda x: x.span()[0])

        tokens = []
        cursor = 0
        for match in matches:
            begin, end = match.span()
            tokens.append(PlainTextToken(text[cursor:begin]))
            if RE_INCLUDES == match.re:
                resolved = (folder / match.group(2)).resolve()
                if not resolved.is_relative_to(folder):
                    raise ValueError(f"Include path escapes template directory: {match.group(2)}")
                tokens.append(TemplateToken(
                    file=(folder / match.group(2)).resolve().absolute(),
                    line_prefix=match.group(1),
                    keep_comments=self._keep_comments))
            elif RE_VARS == match.re:
                tokens.append(PlaceholderToken(text[begin:end]))
            else:
                tokens.append(PlainTextToken(text[begin:end]))
            cursor = end
        tokens.append(PlainTextToken(text[cursor:]))
        return tokens

# ~@:-]
