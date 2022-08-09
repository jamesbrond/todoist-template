"""Abstract class for father of all template loader classes"""

from abc import ABC, abstractmethod

class AbstractTemplateLoader(ABC):
    """Abstract class for father of all template loader classes"""

    @abstractmethod
    def load(self, file):
        """Implement template loading"""

# ~@:-]
