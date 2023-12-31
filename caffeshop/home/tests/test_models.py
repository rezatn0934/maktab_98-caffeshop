from django.test import TestCase
from home.models import About, Gallery, Info
from model_bakery import baker
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
        obj_g = objs.get()
        self.assertEqual(len(objs), 1)
        self.assertEqual(obj_g.cafe_title, "farzam")

    def test_model_failed_save(self):
        failed_save_info = baker.make(Info, cafe_title="reza")
        objs = Info.objects.all()
        obj_g = objs.get()
        self.assertEqual(obj_g.cafe_title, "farzam")
        self.assertTrue(len(objs) == 1)

    def test_delete(self):
        b_length = len(Info.objects.all())

        self.info.delete()

        a_length = len(Info.objects.all())
        self.assertEqual(b_length, a_length)
        self.assertEqual(Info.objects.first().cafe_title, self.info.cafe_title)

    def test_model_update_save(self):
        self.info.cafe_title = "reza"

        self.info.save()

        objs = Info.objects.all()
        obj_g = Info.objects.get(cafe_title="reza")
        self.assertEqual(obj_g.cafe_title, "reza")
        self.assertTrue(len(objs) == 1)

    def test_model_update_save_image(self):
        self.info.logo = SimpleUploadedFile(name='test2_Color_logo_no_background.png', content=open(
            settings.MEDIA_ROOT / "images/test/test2_Color_logo_no_background.png",
            'rb').read(), content_type='image/png')

        self.info.save()

        objs = Info.objects.all()
        obj_g = objs.get()
        self.assertTrue(len(objs) == 1)
        self.assertEqual(str(obj_g.logo).split("/")[-1], "test2_Color_logo_no_background.png")

    def test_model_logo_preview(self):
        logo_preview = self.info.logo_preview()
        self.assertEqual(mark_safe(f'<img src = "{self.info.logo.url}" width = "50" height="80"/> '), logo_preview)

    def test_model_background_image_preview(self):
        background_image_preview = self.info.background_image_preview()
        self.assertEqual(mark_safe(f'<img src = "{self.info.background_image.url}" width = "150" height="150"/> '),
                         background_image_preview)


class TestGalleryModel(TestCase):

    def setUp(self):
        self.gallery = baker.make(Gallery, title="farzam",
                                  image=SimpleUploadedFile(name='test_gallery.jpg', content=open(
                                      settings.MEDIA_ROOT / "images/test/test_gallery.jpg",
                                      'rb').read(), content_type='image/jpg'))

    def tearDown(self):
        self.gallery.delete()

    def test_model_str(self):
        self.assertEqual(str(self.gallery), "farzam")

    def test_delete(self):
        gallery = baker.make(Gallery, title="test_delete",
                             image=SimpleUploadedFile(name='test3_gallery.jpg', content=open(
                                 settings.MEDIA_ROOT / "images/test/test3_gallery.jpg",
                                 'rb').read(), content_type='image/jpg'))
        gallery.delete()
        self.assertFalse(Gallery.objects.filter(title="test_delete").exists())

        image_path = os.path.join(settings.MEDIA_ROOT / "images/gallery", "test3_gallery.jpg")
        self.assertFalse(os.path.exists(image_path))

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
        obj_g = Gallery.objects.get()
        self.assertTrue(len(objs) == 1)
        self.assertEqual(obj_g.title, "reza")
        self.assertEqual(str(obj_g.image).split("/")[-1], "test2_gallery.jpg")


class TestAboutModel(TestCase):
    def setUp(self) -> None:
        self.about = baker.make(About, title="farzam",
                                image=SimpleUploadedFile(name='test_about.jpg', content=open(
                                    settings.MEDIA_ROOT / "images/test/test_about.jpg",
                                    'rb').read(), content_type='image/jpg'),
                                is_active=True)

    def tearDown(self):
        self.about.delete()
        image_path = os.path.join(settings.MEDIA_ROOT / "images/about", "test_about.jpg")
        if os.path.exists(image_path):
            os.remove(image_path)
        image_path2 = os.path.join(settings.MEDIA_ROOT / "images/about", "test2_about.jpg")
        if os.path.exists(image_path2):
            os.remove(image_path2)

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
        obj_g = About.objects.get()

        self.assertTrue(len(objs) == 1)
        self.assertEqual(obj_g.title, "reza")
        self.assertEqual(str(obj_g.image).split("/")[-1], "test2_about.jpg")

    def test_delete(self):
        about = baker.make(About, title="test_delete",
                           image=SimpleUploadedFile(name='test3_about.jpg', content=open(
                               settings.MEDIA_ROOT / "images/test/test3_about.jpg",
                               'rb').read(), content_type='image/jpg'), is_active=False)
        about.delete()
        self.assertFalse(About.objects.filter(title="test_delete").exists())

        image_path = os.path.join(settings.MEDIA_ROOT / "images/about", "test3_about.jpg")
        self.assertFalse(os.path.exists(image_path))

    def test_delete_fail(self):
        about = baker.make(About, title="test_delete_fail",
                           image=SimpleUploadedFile(name='test4_about.jpg', content=open(
                               settings.MEDIA_ROOT / "images/test/test4_about.jpg",
                               'rb').read(), content_type='image/jpg'), is_active=True)
        about.delete()
        self.assertTrue(About.objects.filter(title="test_delete_fail").exists())

        image_path = os.path.join(settings.MEDIA_ROOT / "images/about", "test4_about.jpg")
        self.assertTrue(os.path.exists(image_path))
        os.remove(image_path)

