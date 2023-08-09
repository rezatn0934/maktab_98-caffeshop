from django.contrib.auth.backends import ModelBackend
from .models import User


class PhoneAuthBackend(ModelBackend):

    def authenticate(self, request, phone=None, user_input_otp=None, main_otp=None, **kwargs):
        try:
            user = User.objects.get(phone=phone)
            if user_input_otp and main_otp == user_input_otp:
                return user
        except User.DoesNotExist:
            return

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return
