"""Template token classes"""

from abc import ABC, abstractmethod
from pathlib import Path
import logging
from tplline.tokenizer.tokenizer import (
    RE_VARS,
    RE_INCLUDES,
    RE_PLACEHOLDER,
    RE_FUNC,
    get_template_source_and_folder,
    purge_comments,
    preprocessing_includes,
    preprocessing,
    preprocessing_variables
)
from tplline.tokenizer.func import *  # noqa: F403, F401 pylint: disable=wildcard-import, unused-wildcard-import


class AbstractTemplateToken(ABC):
    """Abstract template token"""

    def __init__(self, text: str, token_type: str) -> None:
        """Initialize the template token with the given text and token type"""
        self._source = text
        self._type = token_type

    @abstractmethod
    def render(self, variables: dict) -> str:
        """Renders the template token"""

    def raw(self) -> str:
        """Returns template token not processed"""
        return self._source

    def __repr__(self) -> str:
        """Returns a string representation of the template token"""
        return f"Token[{self._type}]({self._source})"


class FunctionToken(AbstractTemplateToken):
    """
    Token with function call
    Examples:
        {f[func_name, arg1, arg2]}
    """
    def __init__(self, text):
        super().__init__(text, 'FUNCTION')
        match = RE_FUNC.search(text)
        self._func_name = match.group(1).strip()
        params = match.group(2).split(",") if match.group(2) else []
        self._args = [param.strip() for param in params if param]

    def render(self, variables: dict) -> str:
        return globals()[self._func_name](*self._args) if self._func_name in globals() else self._source


class PlaceholderToken(AbstractTemplateToken):
    """
    Token with placeholder variable

    Examples:
        {username|Guest}
        {due_date}
    """
    def __init__(self, text):
        super().__init__(text, 'PLACEHOLDER')
        match = RE_PLACEHOLDER.search(text)
        self._var_name, self._defval = match.group(1), match.group(2)

    def render(self, variables: dict) -> str:
        return str(variables.get(self._var_name)) if self._var_name in variables else self._defval or self._source


# VariableToken is in the template_token.py to avoid the circular import because it uses TemplateToken
class PlainTextToken(AbstractTemplateToken):
    """
    Simple plain text token

    Example:
        Hello, this is a plain text.
    """

    type = 'PLAINTEXT'

    def __init__(self, text: str):
        super().__init__(text, 'PLAINTEXT')

    def render(self, _) -> str:
        # return plain text as is
        return self._source


class VariableToken(AbstractTemplateToken):
    """
    Token with variable definition.

    Examples:
        {v[username = John Doe]}
        {v[placer_order_number = f[random_sequence, 999@@@@@@@]]}
    """
    def __init__(self, text):
        super().__init__(text, 'VARIABLE')
        match = RE_VARS.search(text)
        self._var_name = match.group(1).strip()
        self._var_value = f"{{{match.group(2).strip()}}}"

    def render(self, variables: dict) -> str:
        token = TemplateToken(text=self._var_value)
        var_value = token.render(variables)
        # store in the render context so later tokens can resolve it
        variables[self._var_name] = var_value
        # remove variable definition from output
        return ""


class TemplateToken(AbstractTemplateToken):
    """
    Parse a template file or string and tokenize it

    Example:
        Hello, {username|Guest}!
        #! include footer.txt
    """

    type = 'TEMPLATE'

    def __init__(self,
                 text: str | None = None,
                 file: Path | None = None,
                 line_prefix: str = "",
                 keep_comments: bool = False):
        super().__init__("", self.type)

        self._filepath = file
        self._line_prefix = line_prefix
        self._keep_comments = keep_comments

        self._source, folder = get_template_source_and_folder(text=text, file=file)

        text = self._source if self._keep_comments else purge_comments(self._source)

        self._tokens = self._compile(text, folder)

    def render(self, variables: dict) -> str:
        """Render template tokens as a single output string"""
        # copy so variable definitions stay scoped to this render pass
        context = dict(variables)
        out = ''
        for token in self._tokens:
            out += token.render(context)

        padding = len(self._line_prefix)
        if padding > 0:
            lines = out.splitlines()
            out = f"{self._line_prefix}{lines[0]}"
            # add padding to all lines but the first one
            if lines[1:]:
                out += "\n" + "\n".join([f"{' ' * padding}{x}" for x in lines[1:]])
        logging.debug("%s\n%s", self._filepath.name if hasattr(self._filepath, "name") else self._filepath, out)
        return out

    def _compile(self, text: str, folder: Path) -> list[AbstractTemplateToken]:
        # parse template source and generate an object ready to be rendered
        matches = [*preprocessing_variables(text), *preprocessing_includes(text), *preprocessing(text)]
        matches.sort(key=lambda x: x.span()[0])
        tokens = []
        cursor = 0
        for match in matches:
            begin, end = match.span()
            if cursor < begin:
                tokens.append(PlainTextToken(text[cursor:begin]))
            if RE_VARS == match.re:
                tokens.append(VariableToken(text[begin:end]))
            elif RE_INCLUDES == match.re:
                tokens.append(TemplateToken(
                    file=(folder / match.group(2)).resolve().absolute(),
                    line_prefix=match.group(1),
                    keep_comments=self._keep_comments))
            elif RE_PLACEHOLDER == match.re:
                tokens.append(PlaceholderToken(text[begin:end]))
            elif RE_FUNC == match.re:
                tokens.append(FunctionToken(text[begin:end]))
            else:
                tokens.append(PlainTextToken(text[begin:end]))
            cursor = end
        tokens.append(PlainTextToken(text[cursor:]))
        return tokens

# ~@:-]
