from django.contrib.auth.backends import ModelBackend
from .models import User
from .form import *


class PhoneAuthBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        phone = kwargs['phone']
        password = kwargs['password']
        try:
            user = User.objects.get(phone=phone)
            if user.check_password(password):
                return user
            else:
                return
        except User.DoesNotExist:
            return

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return
