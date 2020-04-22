# -*- coding: utf-8 -*-
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class UserActivationTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.email_confirmed)
        )


user_activation_token = UserActivationTokenGenerator()