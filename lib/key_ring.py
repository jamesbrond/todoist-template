"""Keyring functions"""

import keyring


def set_api_token(service_id, token):
    """Store token in key ring"""
    keyring.set_password(service_id, "API_TOKEN", token)


def get_api_token(service_id):
    """Get token from key ring"""
    return keyring.get_password(service_id, "API_TOKEN")


def setup(service_id):
    """Prompt user for token"""
    token = input("Please enter your API token: ")
    set_api_token(service_id, token)

# ~@:-]
