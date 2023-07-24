from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.core.validators import RegexValidator
from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    phoneNumberRegex = RegexValidator(regex=r"^09\d{9}$")
    phone = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True)
    first_name = models.CharField(max_length=50, default=" ")
    last_name = models.CharField(max_length=100, default=" ")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone'

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True