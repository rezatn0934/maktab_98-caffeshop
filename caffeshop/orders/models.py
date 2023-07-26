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


