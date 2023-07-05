"""
Secure API Token storage.

It first try to use the python keyring library to provides an easy way to
access the system keyring. If this fails it uses the system environment.
Possibly it may prompt the user for the token and store in the system
keyring or as environment variable.
"""

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
        if os.environ.get(service) is not None:
            os.environ.pop(service)


class APITokenStore:  # pylint: disable=too-few-public-methods
    """
    Secure API Token storage.

    It first try to use the python keyring library to provides an easy way to
    access the system keyring. If this fails it uses the system environment.
    Possibly it may prompt the user for the token and store in the system
    keyring or as environment variable.
    """

    def __init__(self, service, prompt=False) -> None:
        """
        Initilaze `APITokenStore`

        :param service: The name of the service where the `API_TOKEN` is stored.
        :param promt:  is true and there is no stored value it prompts the user for secret
        """
        self.service = service
        self.prompt = prompt
        if isinstance(keyring.get_keyring(), keyring.backends.fail.Keyring):
            keyring.set_keyring(EnvKeyring())

    def _set(self, token):
        """
        Store API token.

        :param token: the value to store.
        """
        keyring.set_password(self.service, "API_TOKEN", token)

    def _get(self):
        """
        Return API token.

        :returns the stored value
        """
        logging.debug("API Token storage: %s", type(keyring.get_keyring()))
        return keyring.get_password(self.service, "API_TOKEN")

    def _prompt(self):
        """
        Prompt user for token.

        :returns the user input value
        """
        return input(_("Please enter your API token: "))

    def get(self):
        """
        Get API Token from keyring or fallback from environment.
        If both methods return `None` and `prompt` is true, it prompts the user for a
        valid API token and store it

        :returns the stored API token.
        """
        api_token = self._get()
        if api_token is None and self.prompt:
            while not api_token:
                logging.warning(_("Todoist API token not found for %s application."), self.service)
                api_token = self._prompt()
            self._set(api_token)
        return api_token

# ~@:-]
