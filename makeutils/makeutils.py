"""Makefile Utilities"""

import sys
import argparse

def is_venv():
    """Check if virtual environment is active"""
    return (hasattr(sys, 'real_prefix') or	(hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--venv', dest="test_venv", default=False, action="store_true")
    args = parser.parse_args()

    if args.test_venv:
        print(int(is_venv()))

# ~@:-]
