from django.db import models
from menu.models import Product, Category
from django.core.validators import RegexValidator, MinValueValidator
# Create your models here.


class Order(models.Model):
    delivery_choices = (('in', 'indoor'), ('out', 'outdoor'))
    status_choices = (('Customer_confirm', (('UC', 'Undetermined'), ('AC', 'Approved'), ('CC', 'Canceled'))),
                      ('Staff_confirm', (('US', 'Undetermined'), ('AS', 'Approved'), ('CS', 'Canceled'))),
                      ('delivery_confirm', (('UD', 'Undetermined'), ('AD', 'Approved'), ('CD', 'Canceled'))))
    phoneNumberRegex = RegexValidator(regex=r"^09\d{9}$")
    phone_number = models.CharField(validators=[phoneNumberRegex], max_length=12)
    date = models.DateTimeField(auto_now=True)
    table_number = models.PositiveIntegerField(validators=[MinValueValidator(0.0)])
    total_price = models.FloatField(validators=[MinValueValidator(0.0)], null=True, blank=True)
    delivery = models.CharField(choices=delivery_choices)
    status = models.CharField(choices=status_choices, default=('Customer_confirm', (('UC', 'Undetermined'))))


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

