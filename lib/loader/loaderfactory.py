"""Implements Factroy Design Pattern to get different template loader according to file type"""

import os
import logging
import mimetypes
from lib.loader.csvloader import CsvTemplateLoader  # pylint: disable=unused-import
from lib.loader.jsonloader import JsonTemplateLoader  # pylint: disable=unused-import
from lib.loader.yamlloader import YamlTemplateLoader  # pylint: disable=unused-import
from lib.i18n import _


TEMPLATE_YAML = "YamlTemplateLoader"
TEMPLATE_JSON = "JsonTemplateLoader"
TEMPLATE_CSV = "CsvTemplateLoader"

MIMETYPES_MAP = {
    "application/json": TEMPLATE_JSON,
    "text/vnd.yaml": TEMPLATE_YAML,
    "text/yaml": TEMPLATE_YAML,
    "text/x-yaml": TEMPLATE_YAML,
    "application/x-yaml": TEMPLATE_YAML,
    "text/csv": TEMPLATE_CSV
}


class TemplateLoaderFactory:  # pylint: disable=too-few-public-methods
    """
    Implements Factroy Design Pattern to get different
    template loader according to file type
    """

    def get_loader(self, file, template_type=None):
        """Returns the right template loader according to file type"""

        template_type = self._guess(file, template_type)
        if template_type is None:
            # if template_type is still None raise exception
            raise ValueError(f"Cannot find template loader for {file.name}")

        loader = globals()[template_type]
        return loader()

    def _guess(self, file, template_type=None):
        if template_type is not None:
            return template_type

        if file.name == '<stdin>':
            # if user do not set template type (ie --yaml, -json, etc)
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
            logging.debug(_("File mimetype %s"), file_mimetype)
            return MIMETYPES_MAP.get(file_mimetype)
        return None

    def _guess_by_extension(self, filepath):
        i, ext = os.path.splitext(filepath)  # pylint: disable=unused-variable
        if not ext.rstrip():
            return None
        if ext in (".yaml", ".yml"):
            logging.debug(_("YAML extension %s"), ext)
            return TEMPLATE_YAML
        if ext == ".json":
            logging.debug(_("JSON extension %s"), ext)
            return TEMPLATE_JSON
        if ext == ".csv":
            logging.debug(_("CSV extension %s"), ext)
            return TEMPLATE_CSV
        return None

# ~@:-]
