"""Keyring functions"""

import os
import logging
import keyring
from lib.i18n import _


def set_api_token(service_id, token):
    """Store token in key ring or fallbacks to environment"""
    try:
        keyring.set_password(service_id, "API_TOKEN", token)
    except keyring.errors.NoKeyringError as err:
        logging.warning(err)
        os.environ[service_id] = token


def get_api_token(service_id):
    """Get token from key ring or from environment as fallback"""
    try:
        return keyring.get_password(service_id, "API_TOKEN")
    except keyring.errors.NoKeyringError as err:
        logging.warning(err)
        return os.environ.get(service_id)


def setup(service_id):
    """Prompt user for token"""
    token = input(_("Please enter your API token: "))
    set_api_token(service_id, token)


def get_keyring_api_token(service_id, prompt=False):
    """Get API Token from keyring or fallback from environment.
    If both methods return `None` and `prompt` is true prompt the user for a
    valid API token and store it"""
    api_token = get_api_token(service_id)
    if api_token is None and prompt:
        while not api_token:
            logging.warning(_("Todoist API token not found for %s application."), service_id)
            setup(service_id)
            api_token = get_api_token(service_id)
    return api_token

# ~@:-]
