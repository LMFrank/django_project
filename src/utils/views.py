from django.contrib.auth.mixins import LoginRequiredMixin
from django import http

from src.utils.response_code import RETCODE


class LoginRequiredJSONMixin(LoginRequiredMixin):
    """
    自定义限制用户访问的扩展类，返回JSON
    """

    def handle_no_permission(self):
        return http.JsonResponse({'code': RETCODE.SESSIONERR, 'errmsg': '用户未登录'})