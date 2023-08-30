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


class TestInfoModelAdminTests(TestCase):

    def setUp(self):
        self.user = baker.make(User, is_active=True, is_staff=True, is_superuser=True)
        self.request = RequestFactory()
        self.request.user = self.user

    def tearDown(self):
        self.user.delete()
        logo_path = os.path.join(settings.MEDIA_ROOT / "images/logo", "test_White_logo_-_no_background.png")
        if os.path.exists(logo_path):
            os.remove(logo_path)

        background_image_path = os.path.join(settings.MEDIA_ROOT / "images/HomePageBackground", "test_intro-bg.jpg")
        if os.path.exists(background_image_path):
            os.remove(background_image_path)

    def test_has_add_permission_first_instance(self):
        info_admin = InfoAdmin(Info, AdminSite())
        self.assertTrue(info_admin.has_add_permission(self.request))

    def test_has_add_permission_next_instance(self):
        self.info = baker.make(Info, cafe_title="farzam",
                               logo=SimpleUploadedFile(name='test_White_logo_-_no_background.png', content=open(
                                   settings.MEDIA_ROOT / "images/test/test_White_logo_-_no_background.png",
                                   'rb').read(), content_type='image/png'),
                               background_image=SimpleUploadedFile(name='test_intro-bg.jpg', content=open(
                                   settings.MEDIA_ROOT / "images/test/test_intro-bg.jpg", 'rb').read(),
                                                                   content_type='image/jpg'))
        info_admin = InfoAdmin(Info, AdminSite())
        self.assertFalse(info_admin.has_add_permission(self.request))
        self.info.delete()

    def test_has_delete_permission(self):
        info_admin = InfoAdmin(Info, AdminSite())
        self.assertFalse(info_admin.has_delete_permission(self.request))


class TestAboutModelAdminTests(TestCase):

    def setUp(self):
        self.user = baker.make(User, is_active=True, is_staff=True, is_superuser=True)
        self.about = baker.make(About, title="about",
                                content="this is a test for truncated content methode in About admin",
                                is_active=True)

        self.about1 = baker.make(About, title="about1", is_active=False,
                                 image=SimpleUploadedFile(name='test2_about.jpg', content=open(
                                     settings.MEDIA_ROOT / "images/test/test2_about.jpg",
                                     'rb').read(), content_type='image/jpg'))
        self.about2 = baker.make(About, title="about2", is_active=False)
        self.factory = RequestFactory()

    def tearDown(self):
        self.user.delete()

        image_path2 = os.path.join(settings.MEDIA_ROOT / "images/about", "test2_about.jpg")
        if os.path.exists(image_path2):
            os.remove(image_path2)

    def test_truncated_content(self):
        about_admin = AboutAdmin(About, AdminSite())
        request = self.factory
        request.user = self.user
        self.assertEqual(about_admin.truncated_content(self.about),
                         "this is a test for truncated content methode in About …")

    def test_delete_about_image(self):
        about_admin = AboutAdmin(About, AdminSite())
        request = self.factory.get(reverse("admin:home_about_changelist"))
        request.user = self.user
        middleware = SessionMiddleware(lambda request: None)
        middleware.process_request(request)
        request.session.save()
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        qs = About.objects.all()
        about_admin.delete_about_image(request, qs)
        qs = About.objects.all()
        self.assertEqual(len(qs), 1)
        self.assertEqual(qs.get().title, "about")
