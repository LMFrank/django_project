# -*- coding: utf-8 -*-
from libs.yuntongxun.ccp_sms import CCP
from celery_tasks.sms import constants
from celery_tasks.main import celery_app
from utils.exceptions import logger


@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):
    """
    发送短信验证码
    :param mobile: 手机号
    :param sms_code: 短信验证码
    :return: 成功或失败
    """
    try:
        res = CCP().send_template_sms(mobile,
                                      [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60],
                                      constants.SEND_SMS_TEMPLATE_ID)
    except Exception as e:
        logger.error(f'发送短信验证码[异常][mobile: {mobile}, message: {e}]')
    else:
        if res == 0:
            logger.info(f'发送短信验证码[正常][mobile: {mobile}]')
        else:
            logger.warning(f'发送短信验证码[失败][mobile: {mobile}]')
