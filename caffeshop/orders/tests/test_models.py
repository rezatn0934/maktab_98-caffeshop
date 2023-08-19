
from django.test import TestCase

from orders.models import Order, Order_detail, Table, Category , Product, User


class TestOrdersModels(TestCase):
    def test_category_models_str(self):
        name = Order.objects.create(id=123)
        self.assertEqual('Order123', str(name))


    def test_get_order_items(self):
        order = Order.objects.create(
        payment='P',
        status='A',
        phone_number='09152593858',
        table_number=Table.objects.create(
        name='orchid',
        Table_number=4,
        occupied=True
        )
        )
        order_item = Order_detail.objects.create(
        order=order,
        product=Product.objects.create(category=Category.objects.create(name='Drinks'),name='Tea',description = 'djf;adjf;ak', price=5.00),
        quantity=1,
        price=10.00
        )


class TestTableModel(TestCase):
    def test_str(self):
        table = Table.objects.create(name='Orchid', Table_number=14, occupied=True)
        self.assertEqual('Orchid', str(table))


