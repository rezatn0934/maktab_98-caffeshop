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
        logo_path = os.path.join(settings.MEDIA_ROOT / "images/logo", "test_White_logo_-_no_background.png")
        if os.path.exists(logo_path):
            os.remove(logo_path)

        background_image_path = os.path.join(settings.MEDIA_ROOT / "images/HomePageBackground", "test_intro-bg.jpg")
        if os.path.exists(background_image_path):
            os.remove(background_image_path)

        logo_path = os.path.join(settings.MEDIA_ROOT / "images/logo", "test2_Color_logo_no_background.png")
        if os.path.exists(logo_path):
            os.remove(logo_path)


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
        self.info.logo = SimpleUploadedFile(name='test2_Color_logo_no_background.png', content=open(
            settings.MEDIA_ROOT / "images/test/test2_Color_logo_no_background.png",
            'rb').read(), content_type='image/png')

        self.info.save()

        objs = Info.objects.all()
        obj_f = Info.objects.filter(cafe_title="farzam")
        obj_g = Info.objects.get(cafe_title="reza")
        self.assertEqual(obj_g.cafe_title, "reza")
        self.assertEqual(str(obj_g.logo).split("/")[-1], "test2_Color_logo_no_background.png")
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


class TestGalleryModel(TestCase):

    def setUp(self) -> None:
        self.gallery = baker.make(Gallery, title="farzam",
                                  image=SimpleUploadedFile(name='test_gallery.jpg', content=open(
                                      settings.MEDIA_ROOT / "images/test/test_gallery.jpg",
                                      'rb').read(), content_type='image/jpg'))

    def tearDown(self):
        self.gallery.delete()

    def test_model_str(self):
        self.assertEqual(str(self.gallery), "farzam")

    def test_model_image_preview(self):
        image_preview = self.gallery.img_preview()
        self.assertEqual(mark_safe(f'<img src = "{self.gallery.image.url}" width = "150" height="150"/> '),
                         image_preview)

    def test_model_update_save(self):
        self.gallery.title = "reza"
        self.gallery.image = SimpleUploadedFile(name='test2_gallery.jpg', content=open(
            settings.MEDIA_ROOT / "images/test/test2_gallery.jpg",
            'rb').read(), content_type='image/jpg')
        self.gallery.save()

        objs = Gallery.objects.all()
        obj_f = Gallery.objects.filter(title="farzam")
        obj_g = Gallery.objects.get(title="reza")

        self.assertEqual(obj_g.title, "reza")
        self.assertTrue(len(objs) == 1)
        self.assertEqual(len(obj_f), 0)
        with self.assertRaises(Http404):
            get_object_or_404(Gallery, title="farzam")


class TestAboutModel(TestCase):
    def setUp(self) -> None:
        self.about = baker.make(About, title="farzam",
                                image=SimpleUploadedFile(name='test_about.jpg', content=open(
                                    settings.MEDIA_ROOT / "images/test/test_about.jpg",
                                    'rb').read(), content_type='image/jpg'),
                                is_active=True)

    def tearDown(self):
        self.about.delete()

    def test_model_str(self):
        self.assertEqual(str(self.about), "farzam")

    def test_model_image_preview(self):
        image_preview = self.about.img_preview()
        self.assertEqual(mark_safe(f'<img src="{self.about.image.url}" width="482" height="316"/>'),
                         image_preview)

    def test_model_update_save(self):
        self.about.title = "reza"
        self.about.image = SimpleUploadedFile(name='test2_about.jpg', content=open(
            settings.MEDIA_ROOT / "images/test/test2_about.jpg",
            'rb').read(), content_type='image/jpg')
        self.about.save()

        objs = About.objects.all()
        obj_f = About.objects.filter(title="farzam")
        obj_g = About.objects.get(title="reza")

        self.assertEqual(obj_g.title, "reza")
        self.assertTrue(len(objs) == 1)
        self.assertEqual(len(obj_f), 0)
        with self.assertRaises(Http404):
            get_object_or_404(About, title="farzam")