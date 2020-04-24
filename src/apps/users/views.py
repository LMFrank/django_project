import re
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django_redis import get_redis_connection


from .models import User
from utils.response_code import RETCODE
from .serializers import UserSerializer


class UsernameCountView(APIView):
    """判断用户名是否已注册"""

    def get(self, request, username):
        """
        判断用户名是否重复
        :param request:
        :param username: 用户名
        :return: JSON
        """
        count = User.objects.filter(username=username).count()
        res_obj = {
            'code': RETCODE.OK,
            'errmsg': 'OK',
            'count': count
        }
        return Response(res_obj)


class MobileCountView(APIView):
    """判断手机号是否已注册"""

    def get(self, request, mobile):
        """
        查询手机号的个数
        :param request:
        :param mobile:
        :return:
        """
        count = User.objects.filter(mobile=mobile).count()
        res_obj = {
            'code': RETCODE.OK,
            'errmsg': 'OK',
            'count': count
        }
        return Response(res_obj)


class UserView(CreateAPIView):
    """用户注册"""

    serializer_class = UserSerializer