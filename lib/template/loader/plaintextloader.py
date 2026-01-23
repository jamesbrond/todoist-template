"""Plain/text Template Loader"""

from lib.template.loader.abstractloader import AbstractTemplateLoader, register_loader


@register_loader
class PlainTextTemplateLoader(AbstractTemplateLoader):  # pylint: disable=too-few-public-methods
    """Plain/text Template Loader"""

    type = "PLAINTEXT"
    mimetypes = ["text/plain"]
    extensions = [".txt"]

    def load(self, content: str) -> any:
        return content.rstrip()
