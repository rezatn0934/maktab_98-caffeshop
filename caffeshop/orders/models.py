from django.db import models
from menu.models import Product, Category
from django.core.validators import MinValueValidator
from utils import phoneNumberRegex


# Create your models here.


class Order(models.Model):
    payment_status = [("U", "unpaid"), ("P", "payed")]
    status_choices = [('P', 'Processing'), ('A', 'Approved'), ('C', 'Canceled')]
    phone_number = models.CharField(validators=[phoneNumberRegex], max_length=11)
    order_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_modify = models.DateTimeField(auto_now=True, editable=False)
    table_number = models.PositiveIntegerField(validators=[MinValueValidator(0.0)])
    status = models.CharField(max_length=1, choices=status_choices, default="P")
    payment = models.CharField(max_length=1, choices=payment_status, default="U")

    def __str__(self):
        return f"Order{self.id}, order total price: {self.total_price}"


class Order_detail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0)]
    )
    total_price = models.FloatField(validators=[MinValueValidator(0.0)], null=True, blank=True)

    def __str__(self):
        return f"order: {self.order}, order item total price: {self.total_price}"
