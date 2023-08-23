from menu.models import Product
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker
from django.conf import settings
from test.support.os_helper import EnvironmentVarGuard
from django.test import TestCase
from utils import send_otp_code, check_availability
from django.urls import reverse
import subprocess
from win32com.shell import shell
import time


class TestUtilsSendOtpCodeCase(TestCase):

    def test_send_otp_code_get_API_exception(self):
        self.env = EnvironmentVarGuard()
        self.env.set('API_KEY', 'value')

        with self.env:
            response = self.client.get(reverse('verify'))
            request = response.wsgi_request
            self.assertEqual(send_otp_code(request, "09117200513"), "API failed")

    def test_send_otp_code_get_HTTP_exception(self):
        response = self.client.get(reverse('verify'))
        request = response.wsgi_request

        result = subprocess.run('netsh wlan show interfaces', capture_output=True, text=True, shell=True)
        output_lines = result.stdout.split('\n')
        lst = []
        for line in output_lines:
            if 'SSID' in line:
                ssid = line.split(':')[1].strip()
                lst.append(ssid)

        commands = 'interface set interface "Wi-Fi" admin=disable'
        shell.ShellExecuteEx(lpVerb='runas', lpFile='netsh.exe', lpParameters=commands)
        time.sleep(10)
        self.assertEqual(send_otp_code(request, "09117200513"), "HTTP connection failed")
        time.sleep(10)
        commands = 'interface set interface "Wi-Fi" admin=enable'
        shell.ShellExecuteEx(lpVerb='runas', lpFile='netsh.exe', lpParameters=commands)
        time.sleep(10)

        command = f'netsh wlan connect name="{lst[0]}" ssid="{lst[0]}"'
        subprocess.run(command, shell=True)


class TestUtilsCheckAvailability(TestCase):

    def setUp(self):
        self.image = open(settings.MEDIA_ROOT / "images/test/pina_colada.png", 'rb').read()
        self.product = baker.make(Product,
                                  image=SimpleUploadedFile.from_dict(
                                      {'filename': 'product_pic1.png', 'content': self.image,
                                       'content_tye': 'image/png'}),
                                  name='Pina Colda', is_active=True)
        self.product1 = baker.make(Product,
                                   image=SimpleUploadedFile.from_dict(
                                       {'filename': 'product_pic2.png', 'content': self.image,
                                        'content_tye': 'image/png'}),
                                   name='not_available', is_active=False)

    def tearDown(self):
        self.product.delete()
        self.product1.delete()

    def test_check_availability(self):
        result = check_availability(self.product)
        self.assertEqual(result[0], f'product {self.product.name} is available')
        self.assertIsNotNone(result[1])

    def test_check_availability_not_available(self):
        result = check_availability(self.product1)
        self.assertEqual(result[0], "Product is not active!!")
        self.assertIsNone(result[1])


