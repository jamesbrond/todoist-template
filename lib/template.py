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

    def __init__(self, tpl_file, file_type=None):
        self._tpl_objects = {} # TODO remove tpl_objects cache as they must be parsed every time
        if tpl_file is None:
            raise TodoistTemplateError("Template file cannot be empty")

        # tpl_object = self._tpl_objects.get(tpl_file.name)

        # if tpl_object is None:
        #     logging.debug("loading template %s (force loader: %s)", tpl_file.name, file_type)

        with tpl_file:
            #tpl_loader = TemplateLoaderFactory().get_loader(tpl_file, file_type)
            #logging.debug("use %s to load '%s' file", tpl_loader.__class__.__name__, tpl_file.name)
            self._tpl_factory = TemplateLoaderFactory(file=tpl_file, template_type=file_type)

    def render(self, variables):
        """
        Loaad the template file using the right loader and return always an array
        even if the template contains only one root element
        """

        # if tpl_file is None:
        #     raise TodoistTemplateError("Template file cannot be empty")

        # tpl_object = self._tpl_objects.get(tpl_file.name)

        # if tpl_object is None:
        #     logging.debug("loading template %s (force loader: %s)", tpl_file.name, file_type)

        #     with tpl_file:
        #         #tpl_loader = TemplateLoaderFactory().get_loader(tpl_file, file_type)
        #         #logging.debug("use %s to load '%s' file", tpl_loader.__class__.__name__, tpl_file.name)
        #         tpl_factory = TemplateLoaderFactory(file=tpl_file, template_type=file_type)
                # tpl_object = tpl_factory.render(variables)
                # self._tpl_objects[tpl_file.name] = tpl_object

        # return tpl_object
        return self._tpl_factory.render(variables)

    # def parse_template(self, tpl_object, variables=None):
    #     """
    #     Parse teplate object and replace all occurrence of variables
    #     """
    #     logging.debug("variables: %s", str(variables))

    #     if not variables:
    #         return tpl_object
    #     return self._replace(tpl_object, variables or {})

    # def _replace(self, obj, variables):
    #     if isinstance(obj, list):
    #         return [self._replace(i, variables) for i in obj]
    #     if isinstance(obj, dict):
    #         return {key: self._replace(value, variables) for key, value in obj.items()}
    #     if isinstance(obj, str):
    #         return self.PLACEHOLDER_REGEXP.sub(
    #             lambda x: variables.get(x.group(1)) or x.group(2),
    #             obj
    #         )
    #     return obj

# ~@:-]
