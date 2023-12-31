from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from django.db.models import Count

from model_bakery import baker
from orders.models import Order, Order_detail
from orders.admin import OrderAdmin, OrderDetailAdmin


class TestOrderAdmin(TestCase):

    def setUp(self):
        self.order1 = baker.make(Order)
        self.order_detail1 = baker.make(Order_detail, order=self.order1)
        self.order_detail2 = baker.make(Order_detail, order=self.order1)
        self.order_detail3 = baker.make(Order_detail, order=self.order1)

    def tearDown(self):
        self.order_detail1.delete()
        self.order_detail2.delete()
        self.order_detail3.delete()
        self.order1.delete()

    def test_order_customer_count_section_url(self):
        order_admin = OrderAdmin(Order, AdminSite())
        expected_link = f'<a href="/admin/orders/order_detail/?order__id={self.order1.id}">{len(Order_detail.objects.filter(order=self.order1))}</a>'
        query_set = Order.objects.filter(id=self.order1.id).annotate(
            customer_count=Count('order_detail')
        )
        order = query_set.get()
        given_link = order_admin.customer_count(order)
        self.assertEqual(expected_link, given_link)

    def test_order_get_query_set(self):
        order_admin = OrderAdmin(Order, AdminSite())
        given_query_set = order_admin.get_queryset(self.client.request)
        self.assertTrue(hasattr(given_query_set.get(), 'customer_count'))
        self.assertEqual(3, given_query_set.get().customer_count)


class TestOrderDetailAdmin(TestCase):

    def setUp(self):
        self.order1 = baker.make(Order)
        self.order_detail1 = baker.make(Order_detail, order=self.order1)

    def tearDown(self):
        self.order_detail1.delete()
        self.order1.delete()

    def test_order_detail_get_order_id(self):
        order_detail_admin = OrderDetailAdmin(Order_detail, AdminSite())
        given_query_set = order_detail_admin.order_id(self.order_detail1)
        self.assertEqual(given_query_set, self.order1.id)
