import re

def strip_emoji(str):
	if str:
		emoji_pattern = re.compile("["
		u"\U0001F600-\U0001F64F"  # emoticons
		u"\U0001F300-\U0001F5FF"  # symbols & pictographs
		u"\U0001F680-\U0001F6FF"  # transport & map symbols
		u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
		"]+", flags=re.UNICODE)
		return emoji_pattern.sub(r'', str).strip()
	return None

def find_needle_in_haystack(needles, haystack, params= [ "name" ]):
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

def dump_json(obj_list):
	for obj in  obj_list:
		print(obj)

# ~@:-]