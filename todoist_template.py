#!/usr/bin/env python

"""UI for Todoist Template"""

import eel
from lib import cli
from lib.config import Config


@eel.expose
def get_api_token():
    """Method called by JavaScript to get API Token"""
    return cli.get_keyring_api_token(cli.DEFAULT_KEYRING_TOKEN_NAME, False)


# Expose this function to Javascript
@eel.expose
def run_script(template, placeholders, api_token, dry_run=False, is_update=False):
    """Method called by JavaScript"""
    cli.run_batch_template(template, [placeholders], api_token, dry_run, is_update, undofile=None)
    return "thanks for running this script"


if __name__ == "__main__":
    cfg = Config()

    eel.init('build/ng', allowed_extensions=['.js', '.html'])

    eel.start(
        'index.html',
        host=cfg.service["host"],
        port=cfg.service["port"],
        mode=cfg.service["mode"],
        cmdline_args=[]
    )

# ~@:-]
