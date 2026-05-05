"""Implements Factroy Design Pattern to get different template loader according to file type"""

import logging
from typing import Any
from template.loader.abstractloader import AbstractTemplateLoader, template_loaders
from template.template_model import TTemplate
from template.template_tokenizer import TemplateToken


class TemplateFactory:  # pylint: disable=too-few-public-methods
    """
    Implements Factroy Design Pattern to get different
    template loader according to file type
    """

    def __init__(self, template: TTemplate, keep_comments: bool = False) -> None:
        # 1. Get the right loader according to file type (YAML, JSON, CSV, Plain/Text)
        self._template = template
        if self._template.type is None:
            # if template type is None raise exception because we aren't able to guess it
            raise ValueError(f"Cannot determine template type for file {str(self._template.file)}")

        if self._template.type not in template_loaders:
            raise ValueError(f"Unknown template type '{self._template.type}' for file {str(self._template.file)}")

        logging.debug('Template type: %s', self._template.type)
        self._loader = template_loaders[self._template.type]()

        # 2. Parse template with tokenizer
        self._tokenizer = TemplateToken(text=template.read(), keep_comments=keep_comments)

    @property
    def template_loader(self) -> AbstractTemplateLoader:
        """Returns the template loader"""
        return self._loader

    @property
    def template_type(self) -> str:
        """Returns the template type"""
        return self._template.type

    @property
    def teamplate_source(self) -> str:
        """Returns the template source"""
        return self._tokenizer._source

    def render(self, variables: dict) -> Any:
        """Returns a template object parsed"""
        # 3. Load the parsed template with the right loader
        logging.debug("render template with variables %s", repr(variables))
        return self._loader.load(self._tokenizer.render(variables))

# ~@:-]
