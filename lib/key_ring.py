import keyring

def set_api_token(service_id, token):
    keyring.set_password(service_id, 'API_TOKEN', token)

def get_api_token(service_id):
    return keyring.get_password(service_id, 'API_TOKEN')

def setup(service_id):
    token = input("Please enter your API token: ")
    set_api_token(service_id, token)

# ~@:-]