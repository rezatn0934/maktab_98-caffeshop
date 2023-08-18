from django.test import SimpleTestCase, Client
from django.urls import reverse
from orders.models import *
import json

class TestUser(SimpleTestCase):
    
    def setUp(self):
        self.client = Client()
        self.cart_url = reverse('cart')
        self.creat_order_url = reverse('create_order')
        self.history_url = reverse('order_history')
        self.cancle_order_url = reverse('cancle_order_by_customer')


    def test_cart_view_GET(self):
        client = self.client.get()
        response=client.get(reverse())