"""Implements Factroy Design Pattern to get different template loader according to file type"""

import os
import logging
import mimetypes
from typing import TextIO
from lib.template.template_tokenizer import TemplateToken
from lib.template.loader.abstractloader import (AbstractTemplateLoader,
                                                template_mimetypes,
                                                template_loaders,
                                                template_extensions)
from lib.template.loader.csvloader import CsvTemplateLoader  # pylint: disable=unused-import
from lib.template.loader.jsonloader import JsonTemplateLoader  # pylint: disable=unused-import
from lib.template.loader.yamlloader import YamlTemplateLoader  # pylint: disable=unused-import
from lib.template.loader.plaintextloader import PlainTextTemplateLoader  # pylint: disable=unused-import


class TodoistTemplateError(Exception):
    """Todoist-Template exception"""

    def __init__(self, message):
        self.message = message


class TemplateFactory:  # pylint: disable=too-few-public-methods
    """
    Implements Factroy Design Pattern to get different
    template loader according to file type
    """

    def __init__(self, file: TextIO, file_type: str | None = None, skip_comments: bool = True):
        # 1. Get the right loader according to file type (YAML, JSON, CSV, Plain/Text)
        self._loader = self.get_loader(file, file_type)
        logging.debug("use %s to load '%s' file", self._loader.__class__.__name__, file.name)

        # ovewrite skip_comments for Plain/Text loader
        keep_comments = self._loader.type == "PLAINTEXT" or not skip_comments

        # 2. Parse template with tokenizer
        self._tokenizer = TemplateToken(file=file, keep_comments=keep_comments)

    def render(self, variables: dict):
        """Returns a template object parsed"""

        logging.debug("render template with %s variables", repr(variables))
        # 3. Load the parsed template with the right loader
        return self._loader.load(self._tokenizer.render(variables))

    def get_loader(self, file: TextIO, file_type: str | None = None) -> AbstractTemplateLoader:
        """Returns the right template loader according to file type"""

        template_type = file_type if file_type is not None else guess_template_type(file)

        if template_type is None:
            # if template_type is still None raise exception
            raise ValueError(f"Cannot determine template type for file {file.name}")

        if template_type not in template_loaders:
            raise ValueError(f"Unknown template type '{template_type}' for file {file.name}")

        logging.debug('Template type: %s', template_type)
        return template_loaders[template_type]()

    @property
    def info(self) -> dict:
        """Returns info about the template factory"""
        return {
            'loader': self._loader.__class__.__name__,
            'template_type': self._loader.type,
            'source': self._tokenizer._source
        }


def guess_template_type(file: TextIO) -> str | None:
    """Guess the template type according to file mimetype or extension"""

    if file.name == '<stdin>':
        # if user do not set template type (ie --yaml, --json, etc)
        # cannot guess the loader from stdin
        return None

    return guess_template_type_by_mimetypes(file.name) or guess_template_type_by_extension(file.name)


def guess_template_type_by_mimetypes(filepath: str) -> str | None:
    """Guess the template type according to file mimetype"""

    file_mimetype, _ = mimetypes.MimeTypes().guess_file_type(filepath)

    if file_mimetype and file_mimetype in template_mimetypes:
        logging.debug("Known file mime-type %s", file_mimetype)
        return template_mimetypes[file_mimetype]

    return None


def guess_template_type_by_extension(filepath: str) -> str | None:
    """Guess the template type according to file extension"""

    _, ext = os.path.splitext(filepath)
    ext = ext.rstrip().lower()

    if ext and ext in template_extensions:
        logging.debug("Know file extension %s", ext)
        return template_extensions[ext]

    return None

# ~@:-]
