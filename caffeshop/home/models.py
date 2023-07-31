from django.db import models
from django.utils.html import mark_safe
from django.db.models.signals import pre_save, post_delete
from caffeshop.signals import change_activation, delete_image_file, change_image


# Create your models here.


class Gallery(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/gallery')

    def img_preview(self):
        if self.image:
            return mark_safe(f'<img src = "{self.image.url}" width = "150" height="150"/> ')

    def __str__(self):
        return self.title


post_delete.connect(delete_image_file, Gallery)
pre_save.connect(change_image, Gallery)


class BackgroundImage(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/HomePageBackground')

    def img_preview(self):
        if self.image:
            return mark_safe(f'<img src = "{self.image.url}" width = "150" height="150"/> ')

    def __str__(self):
        return self.title


post_delete.connect(delete_image_file, BackgroundImage)
pre_save.connect(change_image, BackgroundImage)
pre_save.connect(change_activation, BackgroundImage)
