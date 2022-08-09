import sys

def is_venv():
	return (hasattr(sys, 'real_prefix') or	(hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

if is_venv():
	print(1)
else:
	print(0)