"""Utilities"""

import uuid

def find_needle_in_haystack(needles, haystack, params):
    """Find all needles in the array haystack filtering by params"""
    if len(needles) != len(params):
        return None
    query = dict(zip(params, needles))
    for straw in haystack:
        if all(getattr(straw, k) == v for k, v in query.items()):
            return straw
    return None

def uid():
    """Return UUID"""
    return str(uuid.uuid4())

# ~@:-]
