from django.db import models
from django.utils.html import mark_safe


# Create your models here.


class Gallery(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/gallery')

    def img_preview(self):
        if self.image:
            return mark_safe(f'<img src = "{self.image.url}" width = "150" height="150"/> ')


class BackgroundImage(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/HomePageBackground')

    def img_preview(self):
        if self.image:
            return mark_safe(f'<img src = "{self.image.url}" width = "150" height="150"/> ')
