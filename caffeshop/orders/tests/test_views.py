from django.test import TestCase, Client
from django.urls import reverse
from orders.models import Order, Order_detail, Table
import json


class TestOrdersView(TestCase):
    def test_cart_view_GET(self):
        client = Client()
        response = client.get(reverse('cart'))
