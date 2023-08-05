from django.core.validators import RegexValidator
from django.utils import timezone
from dotenv import load_dotenv
from kavenegar import *
import pyotp
import os

load_dotenv()
phoneNumberRegex = RegexValidator(regex=r"^09\d{9}$")


def send_otp_code(request, phone):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    request.session["otp_code"] = otp
    valid_date = timezone.now() + timezone.timedelta(minutes=1)
    request.session["otp_valid_date"] = str(valid_date)
    try:
        API_KEY = os.environ.get('API_KEY')
        api = KavenegarAPI(API_KEY)

        params = {
            'receptor': f"{phone}",
            'template': 'login',
            'token': f'{otp}',
            'type': 'sms',  # sms vs call
        }
        response = api.verify_lookup(params)

    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def check_availability(obj):
    if obj.is_active:
        message = 'product {obj.name} is available'
        return message, obj
    else:
        message = 'Product is not active!!'
        return message, None


class ImageMixin:
    def change_image(self, old_instance, field):
        target = getattr(old_instance, field)

        if (not target == getattr(self, field) and
                target and os.path.exists(target.path)):
            os.remove(target.path)

    def delete_image(self, field):
        target = getattr(self, field)
        if os.path.exists(target.path):
            os.remove(target.path)
