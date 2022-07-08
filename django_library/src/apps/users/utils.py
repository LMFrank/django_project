# -*- coding: utf-8 -*-
import re
from django.contrib.auth.backends import ModelBackend

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


class UsernameMobileAuthBackend(ModelBackend):
    """自定义用户名/手机号认证"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        验证用户名或手机号，用户既可以使用用户名登录也可以使用手机号
        :param request:
        :param username:
        :param password:
        :param kwargs:
        :return: 用户对象
        """
        try:
            if re.match(r'^1[3-9]\d{9}$', username):
                user = User.objects.get(mobile=username)
            else:
                user = User.objects.get(username=username)
        except:
            user = None
        if user is not None and user.check_password(password):
            return user