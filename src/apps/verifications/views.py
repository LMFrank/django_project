from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
import random

from .libs.captcha.captcha import captcha
from . import constants
from utils.response_code import RETCODE
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
        image_code_server = redis_conn.get(f'img_{uuid}')
        if image_code_server is None:
            res_obj = {'code': RETCODE.IMAGECODEERR,
                       'errmsg': '图形验证码失效'}
            return JsonResponse(res_obj)
        redis_conn.delete(f'img_{uuid}')

        # 对比图形验证码
        image_code_server = image_code_server.decode()
        if image_code_client.lower() != image_code_server.lower():
            res_obj = {'code': RETCODE.IMAGECODEERR,
                       'errmsg': '图形验证码错误'}
            return JsonResponse(res_obj)

        # 生成短信验证码
        # 随机6位数字，不满6位在前面补0
        sms_code = f'{random.randint(0, 999999): 06}'

        # 创建Redis管道
        pl = redis_conn.pipeline()
        pl.setex(f'sms_{mobile}', constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex(f'send_flag_{mobile}', constants.SEND_SMS_CODE_INTERVAL, 1)
        pl.execute()

        ccp_send_sms_code.delay(mobile, sms_code)

        res_obj = {'code': RETCODE.OK,
                   'errmsg': 'OK'}
        return JsonResponse(res_obj)


class ImageCodeView(View):
    """
    图形验证码
    """

    def get(self, request, uuid):
        """
        生成图形验证码
        :param request:
        :param uuid: 图形验证码编号
        :return: image/jdeg
        """
        # 生成图形验证码
        text, image = captcha.generate_captcha()

        # 保存图形验证码字符
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex(f'img_{uuid}', constants.IMAGE_CODE_REDIS_EXPIRES, text)

        return HttpResponse(image, content_type='image/jpeg')





