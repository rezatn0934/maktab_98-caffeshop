from kavenegar import *
import pyotp
from django.utils import timezone


def send_otp_code(request, phone):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    request.session["otp_code"] = otp
    valid_date = timezone.now() + timezone.timedelta(minutes=1)
    request.session["otp_valid_date"] = str(valid_date)
    try:
        api = KavenegarAPI('your API key')

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
