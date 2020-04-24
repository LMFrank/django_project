# -*- coding: utf-8 -*-
import re

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from users.models import User
from verifications.views import SMSCodeView


class UserSerializer(serializers.ModelSerializer):
    """序列化用户信息"""
    password2 = serializers.CharField(min_length=8, max_length=20, write_only=True)
    sms_code = serializers.CharField(min_length=6, max_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2', 'mobile', 'sms_code')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'max_length':20,
                'min_length':8
            },
            'username': {
                'max_length':20,
                'min_length':5
            }
        }

    def validated_mobile(self, mobile):
        """
        验证手机格式
        :param mobile:
        :return:
        """
        if not re.match(r"1[3-9]\d{9}", mobile):
            raise serializers.ValidationError("手机号格式不正确")
        return mobile

    def validate(self, attrs):
        """
        验证密码及短信验证码
        :param attrs:
        :return:
        """
        # 密码
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两次密码不一致')

        # 短信验证码
        real_sms_code = SMSCodeView.check_SMSCode(attrs['mobile'])
        if real_sms_code is None:
            raise serializers.ValidationError('短信验证码过期')
        if real_sms_code != attrs['sms_code']:
            raise serializers.ValidationError('短信验证码错误')

        return attrs

    def create(self, validated_data):
        """
        保存用户数据
        :param validated_data:
        :return:
        """
        # 删除无用数据
        del validated_data['sms_code']
        del validated_data['password2']

        # 保存
        user = User.objects.create_user(**validated_data)

        # 生成token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token

        return user