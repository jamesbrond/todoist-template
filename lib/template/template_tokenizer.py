"""Tokenize template"""
import io
import os
import re
import logging
from enum import Enum
from abc import ABC, abstractmethod


TokenType = Enum('TokenType', ['TEMPLATE', 'PLAINTEXT', 'PLACEHOLDER'])


def read_file(filename, encoding):
    """Get file content"""
    with open(filename, 'r', encoding=encoding) as file:
        text = file.read()
    return text


def get_path(file):
    """Get file path"""
    return os.path.dirname(os.path.realpath(file))


class AbstractToken(ABC):
    """Generic Token Class"""

    RE_INCLUDES = re.compile(r"(.*)#!\s*include +([A-Za-z0-9\/._-]+)")
    RE_VARS = re.compile(r"{(\w+)\s*\|?\s*([^}]+)?}")
    RE_COMMENTS = re.compile(r"(?m)^ *#[^!].*[\n\r]?", re.MULTILINE)
    RE_INLINE_COMMENTS = re.compile(r"\s*#+(?!!).*")
    RE_EMPTY_LINE = re.compile(r"^\s*$\r?\n", re.MULTILINE)

    def __init__(self, text, token_type):
        self._source = text
        self.type = token_type

    @abstractmethod
    def render(self, variables):
        """Render token"""

    def raw(self):
        """Return template not processed"""
        return self._source

    def __str__(self):
        return f"Token({self._source})"


class PlainTextToken(AbstractToken):
    """Plain text token"""
    def __init__(self, text):
        super().__init__(text, TokenType.PLAINTEXT)
        self._source = text

    def render(self, variables):
        return self._source


class PlaceholderToken(AbstractToken):
    """Placeholder token"""
    def __init__(self, text):
        super().__init__(text, TokenType.PLACEHOLDER)
        match = self.RE_VARS.search(text)
        self._value, self._default_value = match.group(1), match.group(2)

    def render(self, variables):
        return variables.get(self._value) or self._default_value or self._source


class TemplateTokenizer(AbstractToken):
    """Parse a template file or string and tokenize it"""
    def __init__(self,
                 text=None,
                 filename=None,
                 folder=None,
                 encoding='utf-8',
                 indent="",
                 skip_comments=True):
        super().__init__(text, TokenType.TEMPLATE)

        self._filename = filename
        self._encoding = encoding
        self._indent = indent
        self._skip_comments = skip_comments

        if text is not None:
            self._source = text
            tempalte_path = get_path(__file__)
        elif filename is not None:
            if isinstance(filename, io.IOBase):
                self._source = filename.read()
                tempalte_path = get_path(filename.name)
            else:
                if folder:
                    path = os.path.join(folder, filename)
                else:
                    path = filename
                self._source = read_file(path, encoding)
                tempalte_path = get_path(path)
        else:
            raise ValueError("TemplateEngine requires text or filename")

        if self._skip_comments:
            text = self._purge_comments(self._source)
        else:
            text = self._source

        self._tokens = self._compile(text, tempalte_path, encoding)

    def render(self, variables):
        """Render template tokens as a single output string"""
        out = ''
        for token in self._tokens:
            out += token.render(variables)

        padding = len(self._indent)
        if padding > 0:
            lines = out.splitlines()
            out = f"{self._indent}{lines[0]}\n"
            # add padding to all lines but the first one
            out += "\n".join([f"{' ' * padding}{x}" for x in lines[1:]])
        logging.debug("%s\n%s", self._filename, out)
        return out

    def _compile(self, text, folder, encoding):
        # parse template source and generate an object ready to be rendered
        matches = [*self._preprocessing_includes(text), *self._preprocessing(text)]
        matches.sort(key=lambda x: x.span()[0])

        tokens = []
        cursor = 0
        for match in matches:
            begin, end = match.span()
            tokens.append(PlainTextToken(text[cursor:begin]))
            if self.RE_INCLUDES == match.re:
                tokens.append(TemplateTokenizer(
                    filename=match.group(2),
                    folder=folder,
                    encoding=encoding,
                    indent=match.group(1),
                    skip_comments=self._skip_comments))
            elif self.RE_VARS == match.re:
                tokens.append(PlaceholderToken(text[begin:end]))
            else:
                tokens.append(PlainTextToken(text[begin:end]))
            cursor = end
        tokens.append(PlainTextToken(text[cursor:]))
        return tokens

    def _purge_comments(self, text):
        # remove all comments lines and inline comments
        txt = text
        txt = re.sub(self.RE_COMMENTS, '', txt)
        txt = re.sub(self.RE_INLINE_COMMENTS, '', txt)
        txt = re.sub(self.RE_EMPTY_LINE, '', txt)
        return txt

    def _includes(self, text):
        yield from self.RE_INCLUDES.finditer(text)

    def _preprocessing_includes(self, text):
        return list(self._includes(text))

    def _tokenize(self, text):
        yield from self.RE_VARS.finditer(text)

    def _preprocessing(self, text):
        return list(self._tokenize(text))

# ~@:-]
