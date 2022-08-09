"""YAML Template Loader"""

import yaml
from lib.loader.CustomYamlLoader import CustomYamlLoader
from lib.loader.abstractloader import AbstractTemplateLoader

class YamlTemplateLoader(AbstractTemplateLoader):
    """YAML Template Class Loader"""

    def load(self, file):
        return yaml.load(file, Loader=CustomYamlLoader)
