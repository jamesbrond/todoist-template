"""Utilities"""
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

# ~@:-]
