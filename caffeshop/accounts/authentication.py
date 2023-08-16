from django.contrib.auth.backends import ModelBackend
from .models import User
from django.utils import timezone

from datetime import datetime


class PhoneAuthBackend(ModelBackend):

    def authenticate(self, request, phone=None, user_input_otp=None, **kwargs):
        try:
            user = User.objects.get(phone=phone)
            otp_valid_date = request.session.get("otp_valid_date")
            if otp_valid_date:
                valid_until = datetime.fromisoformat(otp_valid_date)
                if valid_until > timezone.now():

                    if user_input_otp and request.session.get("otp_code") == user_input_otp:
                        return user
                    else:
                        raise ValueError("Invalid OTP")
                else:
                    raise ValueError("OTP has been expired")
            else:
                raise ValueError("Login First")

        except User.DoesNotExist:
            return

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return
