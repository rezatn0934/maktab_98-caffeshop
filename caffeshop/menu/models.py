from django.db import models
from django.utils.html import mark_safe

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    image = models.ImageField(upload_to='images/category/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def img_preview(self):
        return mark_safe(f'<img src = "{self.image.url}" width = "150" height="150"/> ')


    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=250, unique=True)
    price_per_item = models.FloatField()
    active = models.BooleanField(default=True)
    daily_availability = models.IntegerField(default=0)
    description = models.TextField()
    image = models.ImageField(upload_to='images/product/', blank=True, null=True)

    def img_preview(self):
        return mark_safe(f'<img src = "{self.image.url}" width = "150" height="150"/> ')

    def __str__(self):
        return self.name
