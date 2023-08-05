from django.core.validators import MinValueValidator
from django.db import models
from django.utils.html import mark_safe
import os


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    image = models.ImageField(upload_to='images/category/')

    class Meta:
        verbose_name_plural = "Categories"

    def img_preview(self):
        if self.image:
            return mark_safe(f'<img src = "{self.image.url}" width = "150" height="150"/> ')

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.exists(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = Category.objects.get(pk=self.pk)
            if not old_instance.image == self.image:
                if old_instance.image:
                    if os.path.exists(old_instance.image.path):
                        os.remove(old_instance.image.path)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
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
            if os.path.exists(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = Product.objects.get(pk=self.pk)
            if not old_instance.image == self.image:
                if old_instance.image:
                    if os.path.exists(old_instance.image.path):
                        os.remove(old_instance.image.path)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
