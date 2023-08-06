import json
from functools import lru_cache

import requests

from api_manager.settings import ALMS_IDENTITY_SERVER, ALMS_USER, LABS_API, LABS_USER


@lru_cache(maxsize=None)
def get_alms_token(user=None):
    """
    :param user:
    :return:
    """
    if isinstance(user, str):
        user = json.loads(user)

    response = requests.post(ALMS_IDENTITY_SERVER + '/connect/token', data=user or ALMS_USER, verify=False)
    json_response = response.json()
    return json_response.get('access_token')


@lru_cache(maxsize=None)
def get_labs_token(user=None):
    if isinstance(user, str):
        user = json.loads(user)

    response = requests.post(LABS_API + '/auth/login/', data=user or LABS_USER)
    json_response = response.json()
    return json_response.get('token')
