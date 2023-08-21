from django.test import TestCase, Client
from django.contrib.messages import get_messages
from orders.models import Product, Category
from utils import check_availability 
from orders.cart import just_available_product
from model_bakery import baker

class TestJustAvailableProduct(TestCase):
    def setUp(self):
        self.parent_category = Category.objects.create(name='Food')
        self.category = Category.objects.create(name='fastfood', parent_category=self.parent_category)
        self.product1 = Product.objects.create(name='pizza', price=10, category=self.category)
        self.product2 = Product.objects.create(name='rice', price=20, category=self.category)
        self.orders = {str(self.product1.id): '2', str(self.product2.id): '3'}
        self.client = Client()

    # def test_returns_correct_order_items_and_updated_orders(self):
    #     order_items, updated_orders = just_available_product(self.client, self.orders)
    #     self.assertEqual(len(order_items), 1)
    #     self.assertEqual(order_items[0][0], self.product1)
    #     self.assertEqual(order_items[0][1], 2)
    #     self.assertEqual(order_items[0][2], 20)
    #     self.assertEqual(updated_orders, {str(self.product1.id): '2'})

    # def test_does_not_return_unavailable_products(self):
    #     order_items, updated_orders = just_available_product(self.client.request(), self.orders)
    #     self.assertNotIn(self.product2, [item[0] for item in order_items])
    #     self.assertNotIn(str(self.product2.id), updated_orders.keys())

    # # def test_shows_error_message_for_unavailable_products(self):
    # #     messages = get_messages(self.client)
    # #     order_items, updated_orders = just_available_product(self.client, self.orders)
    # #     self.assertIn('Product 2 is not available!!', [str(m) for m in messages])