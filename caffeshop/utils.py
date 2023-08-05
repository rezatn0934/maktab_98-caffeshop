from django.utils import timezone
from kavenegar import *
import pyotp

def send_otp_code(request, phone):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    request.session["otp_code"] = otp
    valid_date = timezone.now() + timezone.timedelta(minutes=1)
    request.session["otp_valid_date"] = str(valid_date)
    try:
        api = KavenegarAPI('65736836486F3952684276335857666E66443074646F544D79303677342F744C3865624A62673762476A6F3D')

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
    if obj.active:
        message = 'product {obj.name} is available'
        return message, obj
    else:
        message = 'Product is not active!!'
        return message, None
