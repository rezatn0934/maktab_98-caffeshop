from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.utils import timezone


from accounts.models import User
from accounts.views import (
    StaffLogin,
    Verify,
)


class TestStaffLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            phone='09038916990',
            password='reza123456',
            first_name='reza',
            last_name='teymouri'
        )
        self.factory = RequestFactory()

    def test_staff_login_GET_authenticate(self):
        request = self.factory.get(reverse('login'))
        request.user = self.user
        response = StaffLogin.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_staff_login_GET_anonymous(self):
        request = self.factory.get(reverse('login'))
        request.user = AnonymousUser()
        response = StaffLogin.as_view()(request)
        self.assertEqual(response.status_code, 200)

    # def test_staff_login_POST_valid(self):
    #     response = self.client.post(reverse('login'), data={'phone': '09038916990'})
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse('verify'))

    def test_staff_login_POST_invalid(self):
        response = self.client.post(reverse('login'), data={'phone': 'gfhbjnh'})
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertEqual(response.context['message'],
                         'Wrong input, Phone number Should Start 11 digits Like 09*********')
        self.assertFormError(form=response.context['form'], field='phone', errors='Enter a valid value.')


class TestVerify(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            phone='09038916990',
            password='reza123456',
            first_name='reza',
            last_name='teymouri'
        )
        self.factory = RequestFactory()

    def test_verify_GET_authenticate(self):
        request = self.factory.get(reverse('verify'))
        request.user = self.user
        response = Verify.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_verify_GET_anonymous(self):
        request = self.factory.get(reverse('verify'))
        request.user = AnonymousUser()
        middleware = SessionMiddleware(lambda request: None)
        middleware.process_request(request)
        request.session['phone'] = '09038916990'
        request.session.save()

        response = Verify.as_view()(request)
        self.assertEqual(response.status_code, 200)
        del request.session['phone']

    def test_verify_GET_anonymous_not_phone(self):

        request = self.factory.get(reverse('verify'))
        request.user = AnonymousUser()
        middleware = SessionMiddleware(lambda request: None)
        middleware.process_request(request)
        request.session.save()
        response = Verify.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_verify_POST_invalid(self):
        response = self.client.post(reverse('verify'), data={'otp_code': 'jjgh'})
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertEqual(response.context['message'],
                         'Wrong Input')
        self.assertFormError(form=response.context['form'], field='otp_code', errors='Enter a valid value.')

    def test_verify_POST_valid(self):
        request = self.factory.post(reverse('verify'), data={'otp_code': '123456'})
        middleware = SessionMiddleware(lambda request: None)
        request.user = AnonymousUser()
        middleware.process_request(request)
        request.session['otp_code'] = '123456'
        request.session['phone'] = '09038916990'
        request.session['otp_valid_date'] = str(timezone.now())
        valid_date = timezone.now() + timezone.timedelta(minutes=1)
        request.session["otp_valid_date"] = str(valid_date)
        request.session.save()
        setattr(request, '_messages', FallbackStorage(request))
        response = Verify.as_view()(request)
        self.assertEqual(response.status_code, 302)
