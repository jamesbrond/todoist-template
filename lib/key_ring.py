"""Keyring functions"""

import os
import logging
import keyring
import keyring.backend
from lib.i18n import _


class EnvKeyring(keyring.backend.KeyringBackend):
    """A fallback keyring which set and get password from
    operating system environment
    """
    priority = 1

    def set_password(self, service, username, password):
        os.environ[service] = password

    def get_password(self, service, username):
        return os.environ.get(service)

    def delete_password(self, service, username):
        os.environ.pop(service)


class APITokenStore:  # pylint: disable=too-few-public-methods
    """Store and get API token from keyring of fallbacks
    on os environment"""
    def __init__(self, service, prompt=False) -> None:
        self.service = service
        self.prompt = prompt
        if isinstance(keyring.get_keyring(), keyring.backends.fail.Keyring):
            keyring.set_keyring(EnvKeyring())

    def _set(self, token):
        """Store API token"""
        keyring.set_password(self.service, "API_TOKEN", token)

    def _get(self):
        """Return API token"""
        return keyring.get_password(self.service, "API_TOKEN")

    def _prompt(self):
        """Prompt user for token"""
        return input(_("Please enter your API token: "))

    def get(self):
        """Get API Token from keyring or fallback from environment.
        If both methods return `None` and `prompt` is true prompt the user for a
        valid API token and store it"""
        api_token = self._get()
        if api_token is None and self.prompt:
            while not api_token:
                logging.warning(_("Todoist API token not found for %s application."), self.service)
                api_token = self._prompt()
            self._set(api_token)
        return api_token

# ~@:-]
