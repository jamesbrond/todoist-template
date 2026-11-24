"""Localization module"""

import gettext
from todoist_template.__version__ import PACKAGE

gettext.bindtextdomain(PACKAGE, "locales")
gettext.textdomain(PACKAGE)
_t = gettext.gettext

# ~@:-]
