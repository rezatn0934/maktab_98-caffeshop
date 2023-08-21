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



