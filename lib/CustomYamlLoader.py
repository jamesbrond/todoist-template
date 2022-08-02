import logging
import os
import json
import yaml
from typing import Any, IO


class CustomYamlLoader(yaml.SafeLoader):
    """YAML CustomYamlLoader with `!include` constructor."""

    def __init__(self, stream: IO) -> None:
        """Initialise CustomYamlLoader."""

        try:
            self._root = os.path.split(stream.name)[0]
        except AttributeError:
            self._root = os.path.curdir
        super().__init__(stream)


def construct_include(loader: CustomYamlLoader, node: yaml.Node) -> Any:
    """Include file referenced at node."""

    filename = os.path.abspath(
        os.path.join(loader._root, loader.construct_scalar(node))
    )
    extension = os.path.splitext(filename)[1].lstrip(".")
    logging.debug(f"include {filename}")
    with open(filename, "r", encoding="utf8") as f:
        if extension in ("yaml", "yml"):
            return yaml.load(f, CustomYamlLoader)
        elif extension in ("json",):
            return json.load(f)
        else:
            return "".join(f.readlines())

yaml.add_constructor("!include", construct_include, CustomYamlLoader)

# ~@:-]
