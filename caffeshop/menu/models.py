from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from django.db import models

from utils import ImageMixin


# Create your models here.


class Category(ImageMixin, models.Model):
    name = models.CharField(verbose_name=_("Category Name"), max_length=250, unique=True)
    image = models.ImageField(verbose_name=_("Category Image"), upload_to='images/category/')
    parent_category = models.ForeignKey("self", verbose_name=_("Parent Category"), on_delete=models.PROTECT, null=True, blank=True)

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
    category = models.ForeignKey(Category, verbose_name=_("Category"), on_delete=models.PROTECT)
    name = models.CharField(verbose_name=_("Product Name"), max_length=50, unique=True)
    description = models.TextField(verbose_name=_("Product Description"))
    price = models.DecimalField(verbose_name=_("Product Price"), max_digits=5, decimal_places=2)
    is_active = models.BooleanField(verbose_name=_("Active"), default=True)
    image = models.ImageField(verbose_name=_("Product Image"), upload_to='images/product/')

    class Meta:
        permissions = [
            ('change_active_status', 'can change product active status'),
            ('change_price', 'can change product price'),
        ]

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
