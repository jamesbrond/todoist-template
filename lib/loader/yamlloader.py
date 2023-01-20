"""YAML Template Loader"""

import logging
import os
import json
from typing import Any, IO
import yaml
from lib.loader.abstractloader import AbstractTemplateLoader


class CustomYamlLoader(yaml.SafeLoader):  # pylint: disable=too-many-ancestors disable=too-few-public-methods
    """YAML CustomYamlLoader with `!include` constructor."""

    def __init__(self, stream: IO) -> None:
        """Initialise CustomYamlLoader."""

        try:
            self._root = os.path.split(stream.name)[0]
        except AttributeError:
            self._root = os.path.curdir

        super().__init__(stream)

    def get_root(self):
        """Return root path where search for !include files"""
        return self._root


def construct_include(loader: CustomYamlLoader, node: yaml.Node) -> Any:
    """Include file referenced at node."""

    filename = os.path.abspath(
        os.path.join(loader.get_root(), loader.construct_scalar(node))
    )
    extension = os.path.splitext(filename)[1].lstrip(".")
    logging.debug("include %s", filename)
    with open(filename, "r", encoding="utf8") as file:
        if extension in ("yaml", "yml"):
            return yaml.load(file, CustomYamlLoader)
        if extension in ("json",):
            return json.load(file)
        return "".join(file.readlines())


yaml.add_constructor("!include", construct_include, CustomYamlLoader)


class YamlTemplateLoader(AbstractTemplateLoader):  # pylint: disable=too-few-public-methods
    """YAML Template Class Loader"""

    def load(self, file):
        return yaml.load(file, Loader=CustomYamlLoader)
