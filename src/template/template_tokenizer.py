"""Tokenize template"""
import io
import os
import re
import logging
from enum import Enum
from abc import ABC, abstractmethod
from typing import TextIO


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

TEMPLATE_ENCODING: str = 'utf-8'


def read_file(filename: str) -> str:
    """Get file content"""
    with open(filename, 'r', encoding=TEMPLATE_ENCODING) as file:
        text = file.read()
    return text


def get_folder(file: str) -> str:
    """Get file path"""
    return os.path.dirname(os.path.realpath(file))


def get_template(text: str = None, file: str | TextIO = None, base_dir: str = None):
    """Get template source and folder"""

    if text is not None:
        return text, get_folder(__file__)

    if file is not None:
        if isinstance(file, io.IOBase):
            return file.read(), get_folder(file.name)

        path = os.path.join(base_dir, file) if base_dir else file
        return read_file(path), get_folder(path)

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
        self.type = token_type

    @abstractmethod
    def render(self, variables: dict) -> str:
        """Render token"""

    def raw(self) -> str:
        """Return template not processed"""
        return self._source

    def __repr__(self) -> str:
        return f"Token[{self.type.name}]({self._source})"


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
        self._var_name, self._def_value = match.group(1), match.group(2)

    def render(self, variables: dict) -> str:
        return variables.get(self._var_name) or self._def_value or self._source


class TemplateToken(AbstractTemplateToken):
    """
    Parse a template file or string and tokenize it

    Example:
        Hello, {username|Guest}!
        #! include footer.txt
    """
    def __init__(self,  # pylint: disable=too-many-positional-arguments
                 text: str = None,
                 file: str | TextIO = None,
                 base_dir: str = None,
                 line_prefix: str = "",
                 keep_comments: bool = False):
        super().__init__("", TokenType.TEMPLATE)

        self._file = file
        self._line_prefix = line_prefix
        self._keep_comments = keep_comments

        self._source, folder = get_template(text=text, file=file, base_dir=base_dir)

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
        logging.debug("%s\n%s", self._file.name if hasattr(self._file, "name") else self._file, out)
        return out

    def _compile(self, text: str, folder: str) -> list[AbstractTemplateToken]:
        # parse template source and generate an object ready to be rendered
        matches = [*preprocessing_includes(text), *preprocessing(text)]
        matches.sort(key=lambda x: x.span()[0])

        tokens = []
        cursor = 0
        for match in matches:
            begin, end = match.span()
            tokens.append(PlainTextToken(text[cursor:begin]))
            if RE_INCLUDES == match.re:
                tokens.append(TemplateToken(
                    file=match.group(2),
                    base_dir=folder,
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
