import datetime
from datetime import timedelta
import json

import requests
from cacheops import cached
from django.apps import apps
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.exceptions import TokenBackendError, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.utils import aware_utcnow


auth_url = getattr(settings, 'AIIT_AUTH_URL', None)

if not auth_url:
    auth_url = settings.SERVER_URL


def get_token(username, password):
    """
    通过用户名密码获取token
    :param username: 用户名
    :param password: 密码
    :return: 返回 token 的值
    """
    url = '{}/authority/manage/user/login'.format(auth_url)
    payload = json.dumps({
        "password": password,
        "username": username
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    res_json = response.json()
    token = ''
    if res_json:
        try:
            token = res_json.get('result', {}).get('token', '')
        except AttributeError:
            pass
    return token


@cached(timeout=60*10)
def token_validate(jwt_token):
    """
    验证token是否有效
    :param jwt_token: 'Bearer ...'
    :return: 返回 True 或者 False
    """
    url = "{}/authority/token/validate".format(auth_url)
    payload = json.dumps({"token": jwt_token})
    headers = {
        'Authorization': jwt_token,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    res_json = response.json()
    is_valid = res_json.get('result', {}).get('isValid', False)
    return is_valid


@cached(timeout=60*10)
def access_system(jwt_token):
    """
    判断用户是否有此系统的访问权限
    :param jwt_token: 'Bearer ...'
    :return: 返回 True 或者 False
    """

    system_id = getattr(settings, 'AIIT_SYSTEM_ID')
    if not system_id:
        system_id = settings.ROOT_URLCONF.split('.')[0]
    url = "{}/authority/manage/user/verify/access/system".format(auth_url)
    payload = json.dumps(
        {
            "systemId": system_id,
            "token": jwt_token,
        }
    )
    headers = {
        'Authorization': jwt_token,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    res_json = response.json()
    is_valid = res_json.get('result', {}).get('access', False)
    return is_valid


@cached(timeout=60*30)
def token_decode(jwt_token):
    """
    解析 token 的信息，通过 token 获取到 username 之后，如果此用户没有在本系统，系统会自动为本用户创建账号
    :param jwt_token: 'Bearer ...'
    :return: {'username': '', 'user_id': 1, 'exp': 1644917927}
    """
    url = "{}/authority/token/decode".format(auth_url)
    payload = json.dumps({"token": jwt_token})
    headers = {
        'Authorization': jwt_token,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    res_json = response.json()
    payload = res_json.get('result', {})
    username = payload.get('username')
    if username:
        app_name, model_name = settings.AUTH_USER_MODEL.split('.')
        user_model = apps.get_app_config(app_name).get_model(model_name)
        aiit_user, created = user_model.objects.get_or_create(username=username)
        payload['user_id'] = aiit_user.pk
    payload['exp'] = 3600 + int(datetime.datetime.now().timestamp())
    return payload


class AiitToken(UntypedToken):
    lifetime = timedelta(seconds=0)

    def __init__(self, token=None, verify=True):
        self.token = token
        self.current_time = aware_utcnow()

        # Set up token
        if token is not None:
            # # Decode token
            try:
                self.payload = token_decode('Bearer {}'.format(token.decode()))
            except TokenBackendError:
                raise TokenError(_('Token is invalid or expired'))

            if verify:
                self.verify()

    def verify(self):
        is_valid = token_validate('Bearer {}'.format(self.token.decode()))
        if not is_valid:
            raise TokenError(_('token 无效'))
        system_access_check = getattr(settings, 'AIIT_SYSTEM_ACCESS', False)
        if system_access_check:
            can_access = access_system('Bearer {}'.format(self.token.decode()))
            if not can_access:
                raise TokenError(_('无权访问，请联系管理员'))
