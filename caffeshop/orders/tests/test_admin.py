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
