from django.db import models
from django.utils.translation import gettext_lazy as _

from menu.models import Product, Category
from utils import phoneNumberRegex


# Create your models here.


class Order(models.Model):
    payment_status = [("U", "Unpaid"), ("P", "Paid")]
    status_choices = [('P', 'Processing'), ('A', 'Approved'), ('C', 'Canceled')]
    phone_number = models.CharField(verbose_name=_("Phone Number"), validators=[phoneNumberRegex], max_length=11)
    order_date = models.DateTimeField(verbose_name=_("Order Date"), auto_now_add=True, editable=False)
    last_modify = models.DateTimeField(verbose_name=_("Last Modify"), auto_now=True, editable=False)
    table_number = models.ForeignKey("Table", verbose_name=_("Table Name"), on_delete=models.PROTECT, null=True,
                                     blank=True)
    status = models.CharField(verbose_name=_("Order Status"), max_length=1, choices=status_choices, default="P")
    payment = models.CharField(verbose_name=_("Payment Status"), max_length=1, choices=payment_status, default="U")

    @property
    def get_order_items(self):
        order_items = Order_detail.objects.filter(order=self.id)
        return order_items

    @property
    def total_price(self):
        order_detail = self.get_order_items
        order_total_price = 0
        for item in order_detail:
            order_total_price += item.total_price
        return order_total_price

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.table_number:
            table = Table.objects.get(id=self.table_number.id)
            if self.payment == "P" or self.status == 'C':
                table.occupied = False
                table.save()
                return
            table.occupied = True
            table.save()

    def __str__(self):
        return f"Order{self.id}"


class Order_detail(models.Model):
    order = models.ForeignKey(Order, verbose_name=_("Order"), on_delete=models.PROTECT)
    product = models.ForeignKey(Product, verbose_name=_("Product Name"), on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, editable=False)

    class Meta:
        verbose_name_plural = "Order Details"

    @property
    def total_price(self):
        if self.price and self.quantity:
            return self.price * self.quantity
        else:
            return 0

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.price is None:
            self.price = self.product.price
            self.save()

    def __str__(self):
        return f"order: {self.order}"


class Table(models.Model):
    name = models.CharField(verbose_name=_("Table Name"), max_length=50, unique=True)
    Table_number = models.IntegerField(verbose_name=_("Table Number"), unique=True)
    occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"
