"""Run EEL server for todoist-template"""
import os
import sys
import logging
import datetime
import eel
from lib.todoist_template import TodoistTemplate
from lib.config.config import TTConfig
from lib.config.apikey import APITokenStore
from lib.i18n import _


class TTBackendService:  # pylint: disable=too-few-public-methods
    """Run EEL server for todoist-template"""

    def __init__(self, api_token, args):
        self.api_token = api_token
        self.host = args.get("host")
        self.port = args.get("port")
        self.path = args.get("path")

    def start(self):
        """Start web server"""
        eel.init(self.path, allowed_extensions=['.js', '.html'])
        logging.info(_("Service running on http://localhost:%d"), self.port)
        eel.start(
            'index.html',
            host=self.host,
            port=self.port,
            mode=False,
            cmdline_args=[]
        )
        return 0


@eel.expose
def get_api_token():
    """Method called by JavaScript to get API Token"""
    cfg = TTConfig()

    api_token = cfg.config.api_token
    if not api_token:
        # get api_token from keyring or as user input
        api_token_store = APITokenStore(cfg.config.api_key_service, prompt=False)
        api_token = api_token_store.get()
    return api_token


# Expose this function to Javascript
@eel.expose
def run_script(template, placeholders, api_token, dry_run=False, is_update=False):
    """Method called by JavaScript"""
    todoist = TodoistTemplate(api_token, dry_run, False)
    todoist.upload(
        todoist.template({"file": template, "placeholders": placeholders}),
        update_task=is_update)

    if not dry_run:
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        undofolder = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), '.')

        if not os.path.exists(undofolder):
            os.makedirs(undofolder)

        undofile = os.path.join(undofolder, f"gui-{now}.undo")

        todoist.store_rollback(undofile)
    return "thanks for running this script"

# ~@:-]
