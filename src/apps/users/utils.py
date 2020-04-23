# -*- coding: utf-8 -*-
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer, BadData
from django.conf import settings

from .models import User
from . import constants


def generate_verify_email_url(user):
    """
    生成邮箱验证链接，序列化用户信息
    :param user: 要验证邮箱的用户
    :return: 邮箱验证链接
    """
    serializer = TJWSSerializer(settings.SECRET_KEY, expires_in=constants.VERIFY_EMAIL_TOKEN_EXPIRES)
    data = {"user_id": user.id, "email": user.email}
    token = serializer.dumps(data).decode()
    verify_url = settings.EMAIL_VERIFY_URL + '?token=' + token
    return verify_url

def check_verify_email_token(token):
    """
    提取要验证邮箱的用户，反序列化验证链接
    :param token: 邮箱验证链接
    :return: 要验证邮箱的用户
    """
    serializer = TJWSSerializer(settings.SECRET_KEY, expires_in=constants.VERIFY_EMAIL_TOKEN_EXPIRES)
    try:
        data = serializer.loads(token)
    except BadData:
        return None
    else:
        email = data.get("email")
        user_id = data.get("user_id")
        try:
            user = User.objects.get(id=user_id, email=email)
        except User.DoesNotExist:
            return None
        else:
            return user