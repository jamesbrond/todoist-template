"""JSON Template Loader"""

import json
from typing import Any
from template.loader.abstractloader import AbstractTemplateLoader, register_loader


@register_loader
class JsonTemplateLoader(AbstractTemplateLoader):  # pylint: disable=too-few-public-methods
    """JSON Template Class Loader"""

    type = 'JSON'
    mimetypes = ["application/json"]
    extensions = [".json"]

    def load(self, content: str) -> Any:
        """Load JSON template from string content"""
        return json.loads(content)
