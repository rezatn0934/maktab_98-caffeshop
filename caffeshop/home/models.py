from django.utils.html import mark_safe
from utils import phoneNumberRegex
from django.db import models
import os
from django.core.validators import RegexValidator


# Create your models here.


class Gallery(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/gallery')

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
            old_instance = Gallery.objects.get(pk=self.pk)
            if not old_instance.image == self.image:
                if old_instance.image:
                    if os.path.exists(old_instance.image.path):
                        os.remove(old_instance.image.path)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or ''


class Info(models.Model):
    cafe_title = models.CharField(max_length=25)
    cafe_motto = models.TextField()
    phone = models.CharField(validators=[phoneNumberRegex])
    email = models.EmailField()
    work_hours = models.CharField(max_length=100)
    address = models.TextField()
    instagram = models.URLField()
    facebook = models.URLField()
    twitter = models.URLField()
    background_image = models.ImageField(upload_to='images/HomePageBackground')
    logo = models.ImageField(upload_to='images/logo')

    def logo_preview(self):
        if self.logo:
            return mark_safe(f'<img src = "{self.logo.url}" width = "50" height="80"/> ')



class About(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/about')

    def img_preview(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="482" height="316"/>')

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = About.objects.get(pk=self.pk)
            if not old_instance.image == self.image:
                if old_instance.image:
                    if os.path.exists(old_instance.image.path):
                        os.remove(old_instance.image.path)

        objects = About.objects.all()
        if objects:
            objects.update(is_active=False)
        self.is_active = True
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.exists(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title or ''
