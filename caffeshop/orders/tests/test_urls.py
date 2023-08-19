from django.test import SimpleTestCase
from orders.views import CartView, create_order, cancel_order_by_customer, order_history
from django.urls import resolve, reverse

class OrderUrlsTest(SimpleTestCase):
    def test_cart_view_url_is_resolved(self):
        url = reverse('orders:cart')
        self.assertEquals(resolve(url).func.view_class, CartView)
    
    def test_create_order_url_is_resolved(self):
        url = reverse('orders:create_order')
        self.assertEquals(resolve(url).func, create_order)

    def test_order_history_url_is_resolved(self):
        url = reverse('orders:order_history')
        self.assertEquals(resolve(url).func, order_history)

    
    def test_cancel_order_url_is_resolved(self):
        url = reverse('orders:cancel_order_by_customer', args=['1'])
        self.assertEquals(resolve(url).func, cancel_order_by_customer)
