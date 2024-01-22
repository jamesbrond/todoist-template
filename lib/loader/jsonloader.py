"""JOSN Template Loader"""

import json

from lib.loader.abstractloader import AbstractTemplateLoader


class JsonTemplateLoader(AbstractTemplateLoader):  # pylint: disable=too-few-public-methods
    """JSON Template Class Loader"""

    def load(self, content):
        return json.loads(content)
