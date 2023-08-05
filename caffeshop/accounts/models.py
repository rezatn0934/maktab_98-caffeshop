from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from utils import phoneNumberRegex
from .manager import UserManager
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):

    phone = models.CharField(validators=[phoneNumberRegex], unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_modify = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone'

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone
