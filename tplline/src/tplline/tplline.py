"""
TPLline Simple Template engine for python
"""
import sys
from pathlib import Path
from tplline.tokenizer.token import TemplateToken


class TPLLine:
    """Main class"""

    def __init__(self, text: str | None = None, file: Path | None = None, keep_comments: bool = False):
        self._token = TemplateToken(text=text, file=file, line_prefix="", keep_comments=keep_comments)

    @classmethod
    def from_file(cls, file: str | Path, keep_comments: bool = False):
        """
        Create a TPLLine instance from a template file.
        Example:
            tpl = TPLLine.from_file("template.txt")
        """
        return cls(text=None, file=Path(file), keep_comments=keep_comments)

    @classmethod
    def from_stdin(cls, keep_comments: bool = False):
        """
        Create a TPLLine instance from standard input.
        Example:
            tpl = TPLLine.from_stdin()
        """
        template = sys.stdin.read()
        return cls(text=template, keep_comments=keep_comments)

    def render(self, variables: dict) -> str:
        """Render the template with the given variables"""
        return self._token.render(variables)
