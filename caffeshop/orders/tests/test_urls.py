from django.urls import reverse, resolve
from orders.views import *
from django.test import SimpleTestCase

class TestUrls(SimpleTestCase):
    def test_cart_view(self):
        url=reverse('orders:cart')
        self.assertEquals(resolve(url).func.view_class, CartView)

    def test_create_order_view(self):
        url=reverse('orders:create_order')
        self.assertEquals(resolve(url).func, create_order)

    def test_order_history(self):
        url = reverse("orders:order_history")
        self.assertEquals(resolve(url).func, order_history)

    def test_cancle_order(self):
        url = reverse("orders:cancel_order_by_customer", args=['1'])
        self.assertEquals(resolve(url).func, cancel_order_by_customer)
