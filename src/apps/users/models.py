from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    自定义用户类
    """
    mobile = models.CharField(max_length=11, verbose_name="mobile number")
    email_active = models.BooleanField(default=False, verbose_name="email activation status")

    class Meta:
        db_table = "tb_users"
        verbose_name = "User"
        verbose_name_plural = verbose_name

