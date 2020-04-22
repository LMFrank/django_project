# -*- coding: utf-8 -*-
from django.shortcuts import Http404


class StaffRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        print(request.user.is_staff)
        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        raise Http404