from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.html import mark_safe
from django.conf import settings
from django.test import TestCase

from menu.models import Product, Category
from model_bakery import baker

import os

class TestPtoductModel(TestCase):

    def setUp(self):
        self.image = open(settings.MEDIA_ROOT / "images/test/pina_colada.png",'rb').read()
        self.product = baker.make(Product,
         image=SimpleUploadedFile.from_dict({'filename': 'product_pic.png', 'content': self.image, 'content_tye': 'image/png'}),
         name='Pina Colda')

    def tearDown(self):
        if Product.objects.filter(id=self.product.id).exists():
            self.product.delete()

    def test_product_image_preview(self):
        product = self.product
        self.assertEqual(Product.img_preview(self.product), mark_safe(f'<img src = "{self.product.image.url}" width = "150" height="150"/> '))


    def test_product_representation(self):
        self.assertEqual(str(self.product), 'Pina Colda')


    def test_product_deletion(self):
        self.product.delete()
        self.assertFalse(os.path.exists(self.product.image.path))


    def test_product_save_new_image(self):
        new_image = open(settings.MEDIA_ROOT / "images/test/tea.jpg",'rb').read()
        self.product.image = SimpleUploadedFile.from_dict({'filename': 'product_pic2.png', 'content': new_image, 'content_tye': 'image/png'})
        self.product.save()
        self.product = Product.objects.get(id=self.product.id)
        self.assertEqual(open(self.product.image.path, 'rb').read(), new_image)




