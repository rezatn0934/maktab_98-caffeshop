from django.test import TestCase
from orders.models import Category, Product 

class TestOrdersModels(TestCase):
    def test_category_models_str(self):
        name = Category.objects.create(name='django model testing')
        self.assertEqual('django model testing', str(name))
        