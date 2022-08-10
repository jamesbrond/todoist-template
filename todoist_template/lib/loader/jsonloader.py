"""JOSN Template Loader"""

import json

from lib.loader.abstractloader import AbstractTemplateLoader

class JsonTemplateLoader(AbstractTemplateLoader):
    """JSON Template Class Loader"""

    def load(self, file):
        return json.load(file)
