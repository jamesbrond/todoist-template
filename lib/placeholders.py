"""Handle placholders"""
import re


PLACEHOLDER_REGEXP = re.compile(r"{(\w+)\s*\|?\s*([^}]+)?}")


def replace(value, placeholders):
    """Replace placeholders with values"""
    if not isinstance(value, str):
        # {placholder} are always strings
        return value
    return PLACEHOLDER_REGEXP.sub(
        lambda x: placeholders.get(x.group(1)) or x.group(2),
        value
    )


def filter_and_replace_dict(obj, list_keys, placeholders):
    """Filter and replace in dict object"""
    return {k: replace(obj[k], placeholders) for k in list_keys if k in obj}


def filter_and_replace_array(arr, placeholders):
    """Filter and replace in array object"""
    return [replace(k, placeholders) for k in arr]

# ~@:-]
