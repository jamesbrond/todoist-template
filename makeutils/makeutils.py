"""Makefile Utilities"""

import sys

def is_venv():
    """Check if virtual environment is active"""
    return (hasattr(sys, 'real_prefix') or	(hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))


if __name__ == "__main__":
    print(int(is_venv()))

# ~@:-]
