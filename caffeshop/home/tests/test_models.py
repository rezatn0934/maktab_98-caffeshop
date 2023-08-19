from django.test import TestCase
from home.models import About, Gallery, Info
from model_bakery import baker
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings


class TestInfoModel(TestCase):

    def setUp(self) -> None:
        self.info = baker.make(Info, cafe_title="farzam",
                               logo=SimpleUploadedFile(name='test_White_logo_-_no_background.png', content=open(
                                   settings.MEDIA_ROOT / "images/test/test_White_logo_-_no_background.png",
                                   'rb').read(), content_type='image/png'),
                               background_image=SimpleUploadedFile(name='test_intro-bg.jpg', content=open(
                                   settings.MEDIA_ROOT / "images/test/test_intro-bg.jpg", 'rb').read(),
                                                                   content_type='image/jpg'))
