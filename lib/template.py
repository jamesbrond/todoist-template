"""Tansform the template for Todoist-Templete"""

import re
import logging
from lib.loader.loaderfactory import TemplateLoaderFactory


class TodoistTemplateError(Exception):
    """Todoist-Template exception"""


class Template:
    """
    Import a template file and replace placeholders occurrences
    """

    PLACEHOLDER_REGEXP = re.compile(r"{(\w+)\s*\|?\s*([^}]+)?}")

    def load_template(self, tpl_file, file_type=None):
        """
        Loaad the template file using the right loader and return always an array
        even if the template contains only one root element
        """

        if tpl_file is None:
            raise TodoistTemplateError("Template file cannot be empty")

        logging.debug("loading template %s (force loader: %s)", tpl_file.name, file_type)
        with tpl_file:
            tpl_loader = TemplateLoaderFactory().get_loader(tpl_file, file_type)
            logging.debug("use %s to load '%s' file", tpl_loader.__class__.__name__, tpl_file.name)
            tpl_object = tpl_loader.load(tpl_file)

        return tpl_object

    def parse_template(self, tpl_object, placeholders=None):
        """
        Parse teplate object and replace all occurrence of placeholders
        """
        logging.debug("placeholders: %s", str(placeholders))
        if not placeholders:
            return tpl_object
        return self._replace(tpl_object, placeholders or {})

    def _replace(self, obj, placeholders):
        if isinstance(obj, list):
            return [self._replace(i, placeholders) for i in obj]
        if isinstance(obj, dict):
            return {key: self._replace(value, placeholders) for key, value in obj.items()}
        if isinstance(obj, str):
            return self.PLACEHOLDER_REGEXP.sub(
                lambda x: placeholders.get(x.group(1)) or x.group(2),
                obj
            )
        return obj

# ~@:-]
