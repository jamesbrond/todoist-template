"""Plain/text Template Loader"""

from lib.template.loader.abstractloader import AbstractTemplateLoader


class PlainTextTemplateLoader(AbstractTemplateLoader):  # pylint: disable=too-few-public-methods
    """Plain Template Class Loader"""

    def load(self, content):
        return content.rstrip()
