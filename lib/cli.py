"""Command Line Utilities"""
import os
import sys
import logging
import csv
from lib.i18n import _
import lib.key_ring as keyring
from lib.template import TodoistTemplate
from lib.loader.loaderfactory import TemplateLoaderFactory

DEFAULT_KEYRING_TOKEN_NAME = 'TODOIST-TEMPLATE'


def check_python_version():
    """Check the current python version"""
    if sys.version_info < (3, 9) or sys.version_info >= (4, 0):
        raise SystemError(_("This script requires Python >= 3.8 and < 4"))
    return 1


def val_placeholder(values):
    """Argparse placeholders type"""
    placeholders = []
    if os.path.isfile(values):
        with open(values, 'r', encoding='utf8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            placeholders = list(csv_reader)
    else:
        my_dict = {}
        for keyval in values.split(","):
            key, val = keyval.split("=")
            my_dict[key] = val
        placeholders = [my_dict]
    return placeholders


def get_keyring_api_token(service_id, prompt=False):
    """Get API Token from keyring"""
    api_token = keyring.get_api_token(service_id)
    if api_token is None and prompt:
        while not api_token:
            logging.warning(_("Todoist API token not found for %s application."), service_id)
            keyring.setup(service_id)
            api_token = keyring.get_api_token(service_id)
    return api_token


def get_template_content(file):
    """Read template file with the right template loader factory"""
    template_loader = TemplateLoaderFactory().get_loader(file.name)
    logging.debug(_("use %s to load '%s' file"), template_loader.__class__.__name__, file.name)
    return template_loader.load(file)


def undo(undo_file, api_token):
    """Rollback Todoist Actions"""
    tmpl = TodoistTemplate(None, api_token, False, False)  # pylint: disable=too-many-function-args
    tmpl.rollback(undo_file)
    undo_file.close()
    logging.debug(_("remove file %s"), undo_file.name)
    os.remove(undo_file.name)


def run_batch_template(template, placeholders_list, api_token, dry_run, is_update, undofile=None):
    """Run template against a list of placeholders"""
    tmpl = TodoistTemplate(template, api_token, dry_run, is_update)  # pylint: disable=too-many-function-args
    for placeholders in placeholders_list:
        tmpl.parse(template, placeholders, undofile)

# ~@:-]
