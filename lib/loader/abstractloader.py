"""Abstract class for father of all template loader classes"""

from abc import ABC, abstractmethod


class AbstractTemplateLoader(ABC):  # pylint: disable=too-few-public-methods
    """Abstract class for father of all template loader classes"""

    @abstractmethod
    def load(self, file):
        """Implement template loading"""

# ~@:-]
