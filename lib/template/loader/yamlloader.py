"""YAML Template Loader"""

import yaml
from lib.template.loader.abstractloader import AbstractTemplateLoader, register_loader


@register_loader
class YamlTemplateLoader(AbstractTemplateLoader):  # pylint: disable=too-few-public-methods
    """YAML Template Class Loader"""

    type = "YAML"
    mimetypes = ["text/vnd.yaml", "text/yaml", "text/x-yaml", "application/x-yaml", "application/yaml"]
    extensions = [".yaml", ".yml"]

    def load(self, content: str) -> any:
        return yaml.safe_load(content)
