"""Utilities"""
import os
import uuid


def find_needle_in_haystack(haystack, match):
    """
    Find all items in the array `haystack` that have a `match`
    """
    for straw in haystack:
        if isinstance(straw, dict):
            if all(str(straw.get(k)) == str(v) for k, v in match.items()):
                return straw
        else:
            if all(str(getattr(straw, k)) == str(v) for k, v in match.items()):
                return straw

    return None


def uid():
    """Return UUID"""
    return str(uuid.uuid4())


def copy_dict(source, filter_keys):
    """Copy only keys in filter_keys from source dict to a new dict"""
    return {key: value for key, value in source.items() if key in filter_keys}


def read_file(filename: str, encoding: str = "utf-8") -> str:
    """Get file content"""
    with open(filename, 'r', encoding=encoding) as file:
        text = file.read()
    return text


def get_folder(file: str) -> str:
    """Get file path"""
    return os.path.dirname(os.path.realpath(file))

# ~@:-]
