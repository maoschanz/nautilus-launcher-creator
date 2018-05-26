# The python binding for nautilus extensions only recognize .py files in ~/.local/share/nautilus-python
# or in /usr/share/nautilus-python, but i've multiples files and translations so it needs to be in a
# directory.
# This file just calls the actual extension which is in the directory.

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

import BASE_PATH + '/launcher-creator/__init__.py'
