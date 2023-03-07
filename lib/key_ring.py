"""Keyring functions"""

import logging
import keyring
from lib.i18n import _


def set_api_token(service_id, token):
    """Store token in key ring"""
    keyring.set_password(service_id, "API_TOKEN", token)


def get_api_token(service_id):
    """Get token from key ring"""
    return keyring.get_password(service_id, "API_TOKEN")


def setup(service_id):
    """Prompt user for token"""
    token = input(_("Please enter your API token: "))
    set_api_token(service_id, token)


def get_keyring_api_token(service_id, prompt=False):
    """Get API Token from keyring"""
    try:
        api_token = get_api_token(service_id)
        if api_token is None and prompt:
            while not api_token:
                logging.warning(_("Todoist API token not found for %s application."), service_id)
                setup(service_id)
                api_token = get_api_token(service_id)
        return api_token
    except keyring.errors.NoKeyringError as err:
        logging.error(err)
        return None

# ~@:-]
