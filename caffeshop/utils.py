from kavenegar import *


def send_otp_code(phone, code):
    try:
        api = KavenegarAPI('your API key')

        params = {
            'receptor': f"{phone}",
            'template': 'login',
            'token': f'{code}',
            'type': 'sms',  # sms vs call
        }
        response = api.verify_lookup(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
