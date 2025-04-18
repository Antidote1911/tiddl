import logging

from requests import request

from tiddl.exceptions import AuthError
from tiddl.models import auth

AUTH_URL = "https://auth.tidal.com/v1/oauth2"
CLIENT_ID = "zU4XHVVkc2tDPo4t"
CLIENT_SECRET = "VJKhDFqJPqvsPVNBV6ukXTJmwlvbttP7wlMlrc72se4="


logger = logging.getLogger(__name__)


def getDeviceAuth():
    req = request(
        "POST",
        f"{AUTH_URL}/device_authorization",
        data={"client_id": CLIENT_ID, "scope": "r_usr+w_usr+w_sub"},
    )

    data = req.json()

    if req.status_code == 200:
        return auth.AuthDeviceResponse(**data)

    raise AuthError(**data)


def getToken(device_code: str):
    req = request(
        "POST",
        f"{AUTH_URL}/token",
        data={
            "client_id": CLIENT_ID,
            "device_code": device_code,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "scope": "r_usr+w_usr+w_sub",
        },
        auth=(CLIENT_ID, CLIENT_SECRET),
    )

    data = req.json()

    if req.status_code == 200:
        return auth.AuthResponseWithRefresh(**data)

    raise AuthError(**data)


def refreshToken(refresh_token: str):
    req = request(
        "POST",
        f"{AUTH_URL}/token",
        data={
            "client_id": CLIENT_ID,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
            "scope": "r_usr+w_usr+w_sub",
        },
        auth=(CLIENT_ID, CLIENT_SECRET),
    )

    data = req.json()

    if req.status_code == 200:
        return auth.AuthResponse(**data)

    raise AuthError(**data)


def removeToken(access_token: str):
    req = request(
        "POST",
        "https://api.tidal.com/v1/logout",
        headers={"authorization": f"Bearer {access_token}"},
    )

    logger.debug((req.status_code, req.text))
