from django.db import models
from menu.models import Product, Category
from utils import phoneNumberRegex


# Create your models here.


class Order(models.Model):
    payment_status = [("U", "Unpaid"), ("P", "Paid")]
    status_choices = [('P', 'Processing'), ('A', 'Approved'), ('C', 'Canceled')]
    phone_number = models.CharField(validators=[phoneNumberRegex], max_length=11)
    order_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_modify = models.DateTimeField(auto_now=True, editable=False)
    table_number = models.ForeignKey("Table", on_delete=models.PROTECT)
    status = models.CharField(max_length=1, choices=status_choices, default="P")
    payment = models.CharField(max_length=1, choices=payment_status, default="U")

    def __str__(self):
        return f"Order{self.id}"

    @property
    def total_price(self):
        order_detail = Order_detail.objects.filter(order=self.id)
        order_total_price = 0
        for item in order_detail:
            order_total_price += item.total_price
        return order_total_price


class Order_detail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"order: {self.order}"

    @property
    def total_price(self):
        return self.price * self.quantity


class Table(models.Model):
    name = models.CharField(max_length=50, unique=True)
    Table_number = models.IntegerField(unique=True)
    occupied = models.BooleanField(default=False)