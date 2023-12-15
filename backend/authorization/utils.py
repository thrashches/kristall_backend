from enum import Enum
from backend.settings import GOOGLE_OAUTH
from google.oauth2 import id_token
from google.auth.transport import requests


class OauthWay(Enum):
    GOOGLE = 'google'
    VK = 'vk'


def get_user_info(access_token):
    idinfo = id_token.verify_oauth2_token(access_token, requests.Request())
    user_email = idinfo.get('email')
    user_name = idinfo.get('name')
    return user_email, user_name


def create_payload_for_access_google_token(google_credentials,authorization_code):
    data = google_credentials.get('web')
    client_id = data.get('client_id')
    client_secret = data.get('client_secret')
    redirect_uri = data.get('redirect_uris')[0]
    token_url = 'https://oauth2.googleapis.com/token'
    payload = {
        'code': authorization_code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    return payload , token_url


def create_oauth_links(oauth_type: OauthWay):
    try:
        if oauth_type == OauthWay.GOOGLE:
            data = GOOGLE_OAUTH.get('web')
            client_id = data.get('client_id')
            redirect_url = data.get('redirect_uris')[0]
            oauth_link = (f"https://accounts.google.com/o/oauth2/auth?client_id={client_id}&redirect_uri={redirect_url}"
                          f"&scope=profile email&response_type=code")
        elif oauth_type == OauthWay.VK:
            oauth_link = 'is not ready yet'
        else:
            return False, 'We dont support these kind of OAUTH only VK and GOOGLE'
    except Exception as er:
        return False, f"Unexpected error: {er}"
    return oauth_link, ''
