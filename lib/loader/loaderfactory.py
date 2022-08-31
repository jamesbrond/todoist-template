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

    def get_loader(self, filepath):
        """Returns the right template loader according to file type"""

        template_type = self._guess_by_mimetypes(filepath)
        if template_type is None:
            # if mimetypes fail guess by extension
            template_type = self._guess_by_extension(filepath)

            if template_type is None:
                # if template_type is still None raise exception
                raise ValueError(f"Cannot find template loader for {filepath}")

        loader = globals()[template_type]
        return loader()

    def _guess_by_mimetypes(self, filepath):
        file_mimetype = mimetypes.MimeTypes().guess_type(filepath)[0]
        if file_mimetype:
            logging.debug(_("File mimetype %s"), file_mimetype)
            return MIMETYPES_MAP.get(file_mimetype)
        return None

    def _guess_by_extension(self, filepath):
        i, ext = os.path.splitext(filepath)  # pylint: disable=unused-variable
        if ext in (".yaml", ".yml"):
            logging.debug(_("YAML extension %s"), ext)
            return TEMPLATE_YAML
        if ext in (".json"):
            logging.debug(_("JSON extension %s"), ext)
            return TEMPLATE_JSON
        if ext in (".csv"):
            logging.debug(_("CSV extension %s"), ext)
            return TEMPLATE_CSV
        return None

# ~@:-]
