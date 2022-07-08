# -*- coding: utf-8 -*-
import logging
from rest_framework.views import exception_handler as drf_exception_handler
from django.db import DatabaseError
from redis.exceptions import RedisError
from rest_framework.response import Response
from rest_framework import status


logger = logging.getLogger('django')


def exception_handler(exc, context):
    """
    自定义异常处理
    :param exc: 异常
    :param context: 异常上下文
    :return:
    """
    response = drf_exception_handler(exc, context)

    if response is None:
        view = context['view']
        if isinstance(exec, DatabaseError) or isinstance(exec, RedisError):
            # 数据库异常
            logger.error(f'[{view}] exc')
            response = Response({'message': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response

