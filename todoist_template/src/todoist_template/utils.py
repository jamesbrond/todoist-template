"""Utilities"""
import uuid
from pathlib import Path
from typing import Any


def find_needle_in_haystack(haystack: list | dict, match: dict) -> Any | None:
    """
    Return the first item in `haystack` that matches every key/value in `match`
    """
    for straw in haystack:
        if isinstance(straw, dict):
            if all(str(straw.get(k)) == str(v) for k, v in match.items()):
                return straw
        else:
            if all(str(getattr(straw, k, None)) == str(v) for k, v in match.items()):
                return straw

    return None


def uid() -> str:
    """Return UUID"""
    return str(uuid.uuid4())


def copy_dict(source: dict, filter_keys: list[str]) -> dict:
    """Copy only keys in filter_keys from source dict to a new dict"""
    return {key: value for key, value in source.items() if key in filter_keys}


def read_file(filename: str, encoding: str = "utf-8") -> str:
    """Get file content"""
    path = Path(filename)
    with path.open('r', encoding=encoding) as file:
        text = file.read()
    return text


def get_folder(file: str) -> str:
    """Get file path"""
    path = Path(file).resolve()
    return str(path.parent)

# ~@:-]
