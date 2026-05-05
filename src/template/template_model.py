"""Template model module"""

from dataclasses import dataclass
from datetime import datetime
import mimetypes
from pathlib import Path
import sys

from template.loader.abstractloader import template_mimetypes, template_extensions
# Import loaders to register them
from template.loader.plaintextloader import PlainTextTemplateLoader  # noqa F401 pylint: disable=unused-import
from template.loader.jsonloader import JsonTemplateLoader  # noqa F401 pylint: disable=unused-import
from template.loader.yamlloader import YamlTemplateLoader  # noqa F401 pylint: disable=unused-import
from template.loader.csvloader import CsvTemplateLoader  # noqa F401 pylint: disable=unused-import


@dataclass(frozen=True)
class TTemplate:
    """Template options dataclass"""
    file: Path | None = None
    type: str | None = None
    undo_folder: Path | None = None
    undo_file: Path | None = None
    encoding: str = "utf-8"
    stdin: bool = False

    def __post_init__(self):
        # set stdin attribute based on file
        object.__setattr__(self, 'stdin', isinstance(self.file, type(sys.stdin)))

        # set type attribute if not stdin and type is None guessed from file
        if not self.stdin and self.type is None and self.file is not None:
            object.__setattr__(self, 'type', guess_template_type(self.file))

        if self.undo_file is not None:
            object.__setattr__(self, 'undo_folder', self.undo_file.parent.resolve())
        elif self.undo_folder is None:
            object.__setattr__(self, 'undo_folder', Path(__file__).parent.resolve())
        elif isinstance(self.undo_folder, str):
            object.__setattr__(self, 'undo_folder', Path(self.undo_folder).resolve())

    @property
    def undo_file_from_template(self) -> Path:
        """Returns undo file path"""
        suffix = self.file.stem if not self.stdin and self.file else "todoist_template"

        undo_filename = f"{suffix}_{datetime.now().strftime('%Y%m%d%H%M%S')}.undo"
        return self.undo_folder / undo_filename

    def read(self) -> str:
        """Read template content from file or stdin"""
        if self.stdin:
            return sys.stdin.read()
        if self.file is not None and self.file.exists():
            return self.file.read_text(encoding=self.encoding)
        raise ValueError("Template file not found")


def guess_template_type(filepath: Path) -> str | None:
    """Guess the template type according to file mimetype or extension"""
    return guess_template_type_by_mimetypes(filepath) or guess_template_type_by_extension(filepath)


def guess_template_type_by_mimetypes(filepath: Path) -> str | None:
    """Guess the template type according to file mimetype"""
    mime, _ = mimetypes.MimeTypes().guess_file_type(filepath)
    return template_mimetypes[mime] if mime and mime in template_mimetypes else None


def guess_template_type_by_extension(filepath: Path) -> str | None:
    """Guess the template type according to file extension"""
    ext = filepath.suffix.rstrip().lower()
    return template_extensions[ext] if ext and ext in template_extensions else None

# ~@:-]
