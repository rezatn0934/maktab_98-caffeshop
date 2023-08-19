from django.test import TestCase
from home.models import About, Gallery, Info
from model_bakery import baker
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.utils.html import mark_safe
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import os


class TestInfoModel(TestCase):

    def setUp(self) -> None:
        self.info = baker.make(Info, cafe_title="farzam",
                               logo=SimpleUploadedFile(name='test_White_logo_-_no_background.png', content=open(
                                   settings.MEDIA_ROOT / "images/test/test_White_logo_-_no_background.png",
                                   'rb').read(), content_type='image/png'),
                               background_image=SimpleUploadedFile(name='test_intro-bg.jpg', content=open(
                                   settings.MEDIA_ROOT / "images/test/test_intro-bg.jpg", 'rb').read(),
                                                                   content_type='image/jpg'))

    def tearDown(self):
        self.info.delete()
        os.remove(os.path.join(settings.MEDIA_ROOT / "images/logo", "test_White_logo_-_no_background.png"))
        os.remove(os.path.join(settings.MEDIA_ROOT / "images/HomePageBackground", "test_intro-bg.jpg"))

    def test_model_str(self):
        self.assertEqual(str(self.info), "farzam")

    def test_model_save(self):
        objs = Info.objects.all()
        obj_f = Info.objects.filter(cafe_title="farzam")
        obj_g = Info.objects.get(cafe_title="farzam")
        self.assertEqual(len(objs), 1)
        self.assertEqual(len(obj_f), 1)
        self.assertEqual(obj_g.cafe_title, "farzam")

    def test_model_failed_save(self):
        failed_save_info = baker.make(Info, cafe_title="reza")
        objs = Info.objects.all()
        obj_f = Info.objects.filter(cafe_title="reza")
        obj_g = Info.objects.get(cafe_title="farzam")
        self.assertEqual(obj_g.cafe_title, "farzam")
        self.assertTrue(len(objs) == 1)
        self.assertEqual(len(obj_f), 0)
        with self.assertRaises(Http404):
            get_object_or_404(Info, cafe_title="reza")

    def test_model_update_save(self):
        self.info.cafe_title = "reza"
        self.info.save()

        objs = Info.objects.all()
        obj_f = Info.objects.filter(cafe_title="farzam")
        obj_g = Info.objects.get(cafe_title="reza")

        self.assertEqual(obj_g.cafe_title, "reza")
        self.assertTrue(len(objs) == 1)
        self.assertEqual(len(obj_f), 0)
        with self.assertRaises(Http404):
            get_object_or_404(Info, cafe_title="farzam")

    def test_model_logo_preview(self):
        logo_preview = self.info.logo_preview()
        self.assertEqual(mark_safe(f'<img src = "{self.info.logo.url}" width = "50" height="80"/> '), logo_preview)

    def test_model_background_image_preview(self):
        background_image_preview = self.info.background_image_preview()
        self.assertEqual(mark_safe(f'<img src = "{self.info.background_image.url}" width = "150" height="150"/> '),
                         background_image_preview)
