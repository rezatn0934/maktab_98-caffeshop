from django.conf import settings
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, TestCase
from django.urls import reverse

from home.models import Info, About
from accounts.models import User
from home.admin import InfoAdmin, AboutAdmin
from model_bakery import baker
import os


class ModelAdminTests(TestCase):

    def setUp(self):
        self.info = baker.make(Info, cafe_title="farzam",
                               logo=SimpleUploadedFile(name='test_White_logo_-_no_background.png', content=open(
                                   settings.MEDIA_ROOT / "images/test/test_White_logo_-_no_background.png",
                                   'rb').read(), content_type='image/png'),
                               background_image=SimpleUploadedFile(name='test_intro-bg.jpg', content=open(
                                   settings.MEDIA_ROOT / "images/test/test_intro-bg.jpg", 'rb').read(),
                                                                   content_type='image/jpg'))

        self.user = baker.make(User, is_active=True, is_staff=True, is_superuser=True)
        self.about = baker.make(About, content="this is a test for truncated content methode in About admin",
                                is_active=True)

        self.about1 = baker.make(About, title="about1", is_active=False,
                                 image=SimpleUploadedFile(name='test_about.jpg', content=open(
                                     settings.MEDIA_ROOT / "images/test/test_about.jpg",
                                     'rb').read(), content_type='image/jpg'))
        self.about2 = baker.make(About, title="about2", is_active=False)
        self.factory = RequestFactory()

