"""Tokenize template"""
import io
import os
import re
from enum import Enum
from abc import ABC, abstractmethod


TokenType = Enum('TokenType', ['TEMPLATE', 'PLAINTEXT', 'PLACEHOLDER', 'COMMENT'])


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

    RE_INCLUDES = re.compile(r"#!\s*include +([A-Za-z0-9\/._-]+)")
    RE_VARS = re.compile(r"{(\w+)\s*\|?\s*([^}]+)?}")
    RE_COMMENTS = re.compile(r"^#+(?!!).*[\n\r]+", re.MULTILINE)
    RE_INLINE_COMMENTS = re.compile(r" +#+(?!!).*")

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


class CommentToken(AbstractToken):
    """Comment token"""
    def __init__(self, text):
        super().__init__(text, TokenType.COMMENT)

    def render(self, variables):
        return ''


class TemplateTokenizer(AbstractToken):
    """Parse a template file or string and tokenize it"""
    def __init__(self,
                 text=None,
                 filename=None,
                 folder=None,
                 encoding='utf-8'):
        super().__init__(text, TokenType.TEMPLATE)

        self._encoding = encoding

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

        self._tokens = self._compile(self._source, tempalte_path, encoding)

    def render(self, variables):
        """Render template tokens as a single output string"""
        out = ''
        for token in self._tokens:
            out += token.render(variables)

        return out

    def _compile(self, text, folder, encoding):
        # parse template source and generate an object ready to be rendered
        matches = [*self._preprocessing_includes(text), *self._preprocessing(text), *self._preprocessing_comments(text)]
        matches.sort(key=lambda x: x.span()[0])

        tokens = []
        cursor = 0
        for match in matches:
            begin, end = match.span()
            tokens.append(PlainTextToken(text[cursor:begin]))
            if self.RE_INCLUDES == match.re:
                tokens.append(TemplateTokenizer(filename=match.group(1), folder=folder, encoding=encoding))
            elif self.RE_VARS == match.re:
                tokens.append(PlaceholderToken(text[begin:end]))
            else:
                tokens.append(CommentToken(text[begin:end]))
            cursor = end
        tokens.append(PlainTextToken(text[cursor:]))
        return tokens

    def _includes(self, text):
        yield from self.RE_INCLUDES.finditer(text)

    def _preprocessing_includes(self, text):
        return list(self._includes(text))

    def _tokenize(self, text):
        yield from self.RE_VARS.finditer(text)

    def _preprocessing(self, text):
        return list(self._tokenize(text))

    def _comments(self, text):
        yield from self.RE_COMMENTS.finditer(text)

    def _inline_comments(self, text):
        yield from self.RE_INLINE_COMMENTS.finditer(text)

    def _preprocessing_comments(self, text):
        return list(self._comments(text)) + list(self._inline_comments(text))

# ~@:-]
