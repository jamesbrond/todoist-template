"""Localization module"""

import gettext
from __version__ import PACKAGE

gettext.bindtextdomain(PACKAGE, "locales")
gettext.textdomain(PACKAGE)
_ = gettext.gettext


# ~@:-]
