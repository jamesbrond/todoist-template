def find_needle_in_haystack(needles, haystack, params):
    """Find all needles in the array haystack filtering by params"""
    if len(needles) != len(params):
        return None
    for straw in haystack:
        find = True
        for i in range(len(needles)):
            needle = str(needles[i]).lower()
            item = str(getattr(straw, params[i])).lower()
            if needle != item:
                find = False
                break
        if find:
            return straw.id
    return None

# ~@:-]
