from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from django.http import JsonResponse, HttpResponseForbidden
import random

from verifications.libs.captcha.captcha import captcha
from verifications import constants
from src.utils.response_code import RETCODE
from verifications.libs.yuntongxun.ccp_sms import CCP
from celery_tasks.sms.tasks import ccp_send_sms_code


class SMSCodeView(View):
    """
    短信验证码
    """

    def get(self, request, mobile):
        """

        :param request:
        :param mobile: 手机号
        :return: 响应结果
        """
        redis_conn = get_redis_connection('verify_code')
        # 判断用户是否频繁请求发送短信
        send_flag = redis_conn.get(f'send_flag_{mobile}')
        if send_flag:
            res_obj = {'code': RETCODE.THROTTLINGERR,
                       'errmsg': '发送短信过于频繁'}
            return JsonResponse(res_obj)

        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('uuid')

        if not all([image_code_client, uuid]):
            return HttpResponseForbidden('缺少必传参数')

        # 提取图形验证码
        image_code_server = redis_conn.get(f'img_uuid')
        if image_code_server is None:
            res_obj = {'code': RETCODE.IMAGECODEERR,
                       'errmsg': '图形验证码失效'}
            return JsonResponse(res_obj)
        redis_conn.delete(f'img_uuid')

        # 对比图形验证码
        image_code_server = image_code_server.decode()
        if image_code_client.lower() != image_code_server.lower():
            res_obj = {'code': RETCODE.IMAGECODEERR,
                       'errmsg': '图形验证码错误'}
            return JsonResponse(res_obj)

        # 生成短信验证码
        # 随机6位数字，不满6位在前面补0
        sms_code = f'{random.randint(0, 999999): 06d}'
