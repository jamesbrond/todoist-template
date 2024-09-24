"""Implements Factroy Design Pattern to get different template loader according to file type"""

import os
import logging
import mimetypes
from lib.template.template_tokenizer import TemplateTokenizer
from lib.template.loader.csvloader import CsvTemplateLoader  # pylint: disable=unused-import
from lib.template.loader.jsonloader import JsonTemplateLoader  # pylint: disable=unused-import
from lib.template.loader.yamlloader import YamlTemplateLoader  # pylint: disable=unused-import
from lib.template.loader.plaintextloader import PlainTextTemplateLoader  # pylint: disable=unused-import


TEMPLATE_YAML = "YamlTemplateLoader"
TEMPLATE_JSON = "JsonTemplateLoader"
TEMPLATE_CSV = "CsvTemplateLoader"
TEMPLATE_TEXT = "PlainTextTemplateLoader"


MIMETYPES_MAP = {
    "application/json": TEMPLATE_JSON,
    "text/vnd.yaml": TEMPLATE_YAML,
    "text/yaml": TEMPLATE_YAML,
    "text/x-yaml": TEMPLATE_YAML,
    "application/x-yaml": TEMPLATE_YAML,
    "text/csv": TEMPLATE_CSV,
    "text/plain": TEMPLATE_TEXT
}


class TodoistTemplateError(Exception):
    """Todoist-Template exception"""

    def __init__(self, message):
        self.message = message


class TemplateFactory:  # pylint: disable=too-few-public-methods
    """
    Implements Factroy Design Pattern to get different
    template loader according to file type
    """

    def __init__(self, file, file_type=None, is_quick_add=False):
        self._tokenizer = TemplateTokenizer(filename=file, skip_comments=not is_quick_add)

        self._loader = self.get_loader(file, file_type)
        logging.debug("use %s to load '%s' file", self._loader.__class__.__name__, file.name)

    def render(self, variables):
        """Returns a template object parsed"""

        logging.debug("render template with %s variables", str(variables))
        return self._loader.load(self._tokenizer.render(variables))

    def get_loader(self, file, file_type=None):
        """Returns the right template loader according to file type"""

        template_type = file_type if file_type is not None else self._guess(file)
        if template_type is None:
            # if template_type is still None raise exception
            raise ValueError(f"Cannot find template loader for {file.name}")
        logging.debug('template type: %s', template_type)
        loader = globals()[template_type]
        return loader()

    def _guess(self, file):
        if file.name == '<stdin>':
            # if user do not set template type (ie --yaml, --json, etc)
            # do not guess the loader from stdin
            return None

        template_type = self._guess_by_mimetypes(file.name)
        if template_type is not None:
            return template_type

        template_type = self._guess_by_extension(file.name)
        return template_type

    def _guess_by_mimetypes(self, filepath):
        file_mimetype = mimetypes.MimeTypes().guess_type(filepath)[0]
        if file_mimetype:
            logging.debug("File mimetype %s", file_mimetype)
            return MIMETYPES_MAP.get(file_mimetype)
        return None

    def _guess_by_extension(self, filepath):
        _, ext = os.path.splitext(filepath)
        if not ext.rstrip():
            return None
        if ext in (".yaml", ".yml"):
            logging.debug("YAML extension %s", ext)
            return TEMPLATE_YAML
        if ext == ".json":
            logging.debug("JSON extension %s", ext)
            return TEMPLATE_JSON
        if ext == ".csv":
            logging.debug("CSV extension %s", ext)
            return TEMPLATE_CSV
        if ext == ".txt":
            logging.debug("Plain/Text extension %s", ext)
            return TEMPLATE_TEXT
        return None

# ~@:-]
