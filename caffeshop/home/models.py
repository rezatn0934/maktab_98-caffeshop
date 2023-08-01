from django.db import models
from django.utils.html import mark_safe
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


class BackgroundImage(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/HomePageBackground')

    def img_preview(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="150" height="150"/>')

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.exists(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = BackgroundImage.objects.get(pk=self.pk)
            if not old_instance.image == self.image:
                if old_instance.image:
                    if os.path.exists(old_instance.image.path):
                        os.remove(old_instance.image.path)
        BackgroundImage.objects.all().update(is_active=False)
        self.is_active = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or ''


class Info(models.Model):
    phoneNumberRegex = RegexValidator(regex=r"^09\d{9}$")
    phone = models.CharField(validators=[phoneNumberRegex])
    email = models.EmailField()
    work_hours = models.CharField(max_length=100)
    address = models.TextField()
    instagram = models.URLField()
    facebook = models.URLField()
    twitter = models.URLField()


class Logo(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/logo')


    def img_preview(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50" height="80"/>')

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.exists(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)


class About(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/about')

    def img_preview(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50" height="80"/>')

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = About.objects.get(pk=self.pk)
            if not old_instance.image == self.image:
                if old_instance.image:
                    if os.path.exists(old_instance.image.path):
                        os.remove(old_instance.image.path)
        About.objects.all().update(is_active=False)
        self.is_active = True
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.exists(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
