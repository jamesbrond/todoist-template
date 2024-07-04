"""YAML Template Loader"""

import yaml
from lib.template.loader.abstractloader import AbstractTemplateLoader


class YamlTemplateLoader(AbstractTemplateLoader):  # pylint: disable=too-few-public-methods
    """YAML Template Class Loader"""

    def load(self, content):
        return yaml.safe_load(content)
