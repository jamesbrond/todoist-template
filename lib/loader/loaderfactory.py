"""Implements Factroy Design Pattern to get different template loader according to file type"""

import os
import logging
import mimetypes
from lib.loader.csvloader import CsvTemplateLoader
from lib.loader.jsonloader import JsonTemplateLoader
from lib.loader.yamlloader import YamlTemplateLoader

TEMPLATE_YAML = 1
TEMPLATE_JSON = 2
TEMPLATE_CSV  = 3

MIMETYPES_MAP = {
    "application/json": TEMPLATE_JSON,
    "text/vnd.yaml": TEMPLATE_YAML,
    "text/yaml": TEMPLATE_YAML,
    "text/x-yaml": TEMPLATE_YAML,
    "application/x-yaml": TEMPLATE_YAML,
    "text/csv": TEMPLATE_CSV
}

class TemplateLoaderFactory:
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

        if template_type == TEMPLATE_YAML:
            return YamlTemplateLoader()
        if template_type == TEMPLATE_JSON:
            return JsonTemplateLoader()
        if template_type == TEMPLATE_CSV:
            return CsvTemplateLoader()

    def _guess_by_mimetypes(self, filepath):
        file_mimetype = mimetypes.MimeTypes().guess_type(filepath)[0]
        if file_mimetype:
            logging.debug("File mimetype %s", file_mimetype)
            return MIMETYPES_MAP.get(file_mimetype)
        return None

    def _guess_by_extension(self, filepath):
        _, ext = os.path.splitext(filepath)
        if ext in (".yaml", ".yml"):
            logging.debug("YAML extension %s", ext)
            return TEMPLATE_YAML
        if ext in (".json"):
            logging.debug("JSON extension %s", ext)
            return TEMPLATE_JSON
        return None

# ~@:-]
