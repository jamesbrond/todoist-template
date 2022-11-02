#!/usr/bin/env python

"""UI for Todoist Template"""

import eel
from lib import cli


@eel.expose
def get_api_token():
    """Method called by JavaScript to get API Token"""
    return cli.get_keyring_api_token(cli.DEFAULT_KEYRING_TOKEN_NAME, False)


# Expose this function to Javascript
@eel.expose
def run_script(filename, template, placeholders, api_token, dry_run=False, is_update=False):
    """Method called by JavaScript"""
    print(f"filename: {filename}")
    print(f"template: {template}")
    print(f"placeholders: {placeholders}")
    print(f"api token: {api_token}")
    print(f"is dry run? {dry_run}")
    print(f"is update? {is_update}")

    cli.run_batch_template(template, [placeholders], api_token, dry_run, is_update, undofile=None)
    return "thanks for running this script"


if __name__ == "__main__":
    eel.init('build/ng', allowed_extensions=['.js', '.html'])

    eel.start(
        'index.html',
        port=54321,
        cmdline_args=[]
    )

# ~@:-]
