from django.test import TestCase, Client
from django.urls import reverse
from home.models import About, Gallery
from menu.models import Category, Product
from model_bakery import baker
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import os


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
        image_path = os.path.join(settings.MEDIA_ROOT / "images/about", "test_about.jpg")
        if os.path.exists(image_path):
            os.remove(image_path)

    def test_home_GET(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/home.html")
        self.failUnless(response.context["categories"], self.categories)
        self.failUnless(response.context["gallery"], self.galleries)
        self.failUnless(response.context["about"], self.abouts)
