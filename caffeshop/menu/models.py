from django.core.validators import MinValueValidator
from django.utils.html import mark_safe
from utils import ImageMixin
from django.db import models
import os


# Create your models here.


class Category(ImageMixin, models.Model):
    name = models.CharField(max_length=250, unique=True)
    image = models.ImageField(upload_to='images/category/')
    parent_category = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def img_preview(self):
        if self.image:
            return mark_safe(f'<img src = "{self.image.url}" width = "150" height="150"/> ')

    def delete(self, *args, **kwargs):
        if self.image:
            self.delete_image("image")
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = Category.objects.get(pk=self.pk)
            self.change_image(old_instance, "image")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(ImageMixin, models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    price_per_item = models.DecimalField(validators=[MinValueValidator(0.0)])
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/product/')

    def img_preview(self):
        if self.image:
            return mark_safe(f'<img src = "{self.image.url}" width = "150" height="150"/> ')

    def delete(self, *args, **kwargs):
        if self.image:
            self.delete_image("image")
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = Product.objects.get(pk=self.pk)
            self.change_image(old_instance, "image")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
