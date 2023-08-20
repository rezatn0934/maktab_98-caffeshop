from django.test import TestCase
from orders.models import Order, Order_detail, Table, Category , Product, User


class TestOrdersModels(TestCase):
    def test_category_models_str(self):
        name = Order.objects.create(id=123)
        self.assertEqual('Order123', str(name))


    def test_get_order_detatils(self):
        order = Order.objects.create(
        payment='P',
        status='A',
        phone_number='09152593858',
        table_number=Table.objects.create(
        name='orchid',
        Table_number=4,
        occupied=True))
        order_item = Order_detail.objects.create(
        order=order,
        product=Product.objects.create(category=Category.objects.create(name='Drinks'),name='Tea',description = 'djf;adjf;ak', price=5.00),
        quantity=1,
        price=10.00)

    def setUp(self):
        self.order = Order.objects.create(
            payment='P',
            status='A',
            phone_number='09152593858',
            table_number=Table.objects.create(name='rose',Table_number=6,occupied=True),
            order_date='2021-01-01',
        )
        self.order_item1 = Order_detail.objects.create(
            order=self.order,
            product=Product.objects.create(category=Category.objects.create(name='Foods'),name='rice',description = 'djf;adjf;ak', price=8.00),
            quantity=1,
        )
        self.order_item2 = Order_detail.objects.create(
            order=self.order,
            product =Product.objects.create(category=Category.objects.create(name='FastFood'),name='hamburger',description = 'jjjjjj', price=6.00),
            quantity=3,
        )

    def test_get_order_items(self):
        order = Order.objects.create(payment='P',status='A',phone_number='09152593858',table_number=Table.objects.create(
        name='orchid',Table_number=4,occupied=True))
        order_items = Order_detail.objects.create(order=order,
        product=Product.objects.create(category=Category.objects.create(name='Drinks'),name='Tea',description = 'djf;adjf;ak', price=5.00),
        quantity=1,price=10.00)
        order_products = Order_detail.objects.get(order=order.id)
        self.assertEqual(order_products, order_items)
        order_items = self.order.get_order_items
        self.assertEqual(order_items.count(), 2)
        self.assertEqual(order_items[0].product.name, 'rice')
        self.assertEqual(order_items[1].product.name, 'hamburger')

    # def setup(self):
    #     self.order = Order.objects.create(
    #         payment = 'P',
    #         status = 'A',
    #         phone_number ='09152593858',
    #         table_number = Table.objects.create(name='rose', Table_number = 20, occupied=True),
    #         order_date = '2023-07-31'
    #     )
    def test_str(self):
        self.assertEquals(str(self.order), 'Order8')

    def test_total_price(self):
        order = Order.objects.create(
            status = 'A',
            payment = 'P',
            phone_number = '09152593858',
            table_number = Table.objects.create(name='violet', Table_number=60, occupied = True)
        )
        order_detail = Order_detail.objects.create(order=self.order,product=Product.objects.get(name='hamburger'),quantity=2, price=10.00)
        self.assertEqual(order_detail.total_price, 20.0)

    def test_total_order_price(self):
        order = Order(
            payment='P',
            status='A',
            phone_number='09152593858',
            table_number=Table.objects.create(name='lavander',Table_number=13,occupied=True),
            order_date='2023-03-03',
        )
        order_detail = Order_detail(
            order = order,
            product= Product.objects.create(category = Category.objects.create(name='hotdrinks'), name='Coffee', price=10.00, description='ffffff'),
            quantity=1,
            price=100
        )
        order_detail1 = Order_detail(
            order=order,
            product = Product.objects.create(category=Category.objects.create(name='colddrinks'), name='soda', price=30.00, description='cold drink'),
            quantity=3,
            price=30
        )
        self.assertEqual(order.total_price, 0)

    def test_has_no_quantity(self):
        
        pass
        

    def test_save(self):
        self.order.save()
        self.assertEqual(str(self.order.phone_number), '09152593858')
        self.assertEqual(str(self.order.table_number), 'rose')
      
class TestTableModel(TestCase):
    def test_str(self):
        table = Table.objects.create(name='Orchid', Table_number=14, occupied=True)
        self.assertEqual('Orchid', str(table))
