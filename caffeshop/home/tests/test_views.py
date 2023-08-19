from django.test import TestCase, Client
from django.urls import reverse
from home.models import About, Gallery
from menu.models import Category, Product
from model_bakery import baker
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings


class TestHomeView(TestCase):

    def setUp(self):
        self.gallery = baker.make(Category, image=SimpleUploadedFile(name='test_category.jpg', content=open(
            settings.MEDIA_ROOT / "images/test/test_category.jpg",
            'rb').read(), content_type='image/jpg'))
        self.category = baker.make(Gallery, image=SimpleUploadedFile(name='test_gallery.jpg', content=open(
            settings.MEDIA_ROOT / "images/test/test_gallery.jpg",
            'rb').read(), content_type='image/jpg'))
        self.about = baker.make(About, image=SimpleUploadedFile(name='test_about.jpg', content=open(
            settings.MEDIA_ROOT / "images/test/test_about.jpg",
            'rb').read(), content_type='image/jpg'))

        self.client = Client()
        self.galleries = Gallery.objects.filter(is_active=True)
        self.categories = Category.objects.all()
        self.abouts = About.objects.get(is_active=True)

    def tearDown(self):
        self.gallery.delete()
        self.category.delete()
        self.about.delete()

