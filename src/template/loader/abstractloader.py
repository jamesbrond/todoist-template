"""Abstract class used as father of all template loader classes inheriting from it"""

from abc import ABC, abstractmethod
from typing import Any

# e.g. 'YAML': YamlTemplateLoader
template_loaders: dict[str, AbstractTemplateLoader] = {}

# e.g. 'application/json': 'JSON'
template_mimetypes: dict[str, str] = {}

# e.g. '.json': 'JSON'
template_extensions: dict[str, str] = {}


def register_loader(cls: AbstractTemplateLoader):
    """Class decorator used to register template loader classes"""
    if issubclass(cls, AbstractTemplateLoader):
        if bool(cls.type) and cls.type not in template_loaders:
            template_loaders[cls.type] = cls
        for mimetype in cls.mimetypes:
            template_mimetypes[mimetype] = cls.type
        for ext in cls.extensions:
            template_extensions[ext] = cls.type
    return cls


class AbstractTemplateLoader(ABC):  # pylint: disable=too-few-public-methods
    """Abstract class used as father of all template loader classes inheriting from it"""

    type: str | None = None
    mimetypes: list[str] = []
    extensions: list[str] = []

    @abstractmethod
    def load(self, content: str) -> Any:
        """Implements template parsing from string"""

# ~@:-]
