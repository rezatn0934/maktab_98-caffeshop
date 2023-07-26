from django.db import models
from menu.models import Product, Category
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
# Create your models here.


class Order(models.Model):
    phoneNumberRegex = RegexValidator(regex=r"^09\d{9}$")
    phone_number = models.CharField(validators=[phoneNumberRegex], unique=True , max_length=12)
    date = models.DateTimeField(auto_now=True)
    table_number = models.PositiveIntegerField(validators=[MinValueValidator(0.0),])
    total_price = models.FloatField( validators=[MinValueValidator(0.0),], null=True, blank=True)

    def __str__(self):
        return f"Order{self.id}, order total price: {self.total_price}"




class Order_detail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(null=True, blank=True)
    total_price = models.FloatField(validators=[MinValueValidator(0.0),], null=True, blank=True)

    def __str__(self):
        return f"order: {self.order}, order item total price: {self.total_price}"

