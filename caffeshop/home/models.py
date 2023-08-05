from django.utils.html import mark_safe
from utils import phoneNumberRegex, ImageMixin
from django.db import models


# Create your models here.


class Gallery(ImageMixin, models.Model):
    title = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/gallery')

    def img_preview(self):
        if self.image:
            return mark_safe(f'<img src = "{self.image.url}" width = "150" height="150"/> ')

    def delete(self, *args, **kwargs):
        if self.image:
            self.delete_image("image")

        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = Gallery.objects.get(pk=self.pk)
            self.change_image(old_instance, "image")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Info(ImageMixin, models.Model):
    cafe_title = models.CharField(max_length=25)
    cafe_motto = models.TextField()
    phone = models.CharField(validators=[phoneNumberRegex])
    email = models.EmailField()
    work_hours = models.CharField(max_length=100)
    address = models.TextField()
    instagram = models.URLField()
    facebook = models.URLField()
    twitter = models.URLField()
    max_table_number = models.PositiveIntegerField()
    background_image = models.ImageField(upload_to='images/HomePageBackground')
    logo = models.ImageField(upload_to='images/logo', null=True, blank=True)

    @classmethod
    def get_max_table_number(cls):
        info_obj = cls.objects.get()
        return info_obj.max_table_number

    def logo_preview(self):
        if self.logo:
            return mark_safe(f'<img src = "{self.logo.url}" width = "50" height="80"/> ')

    def background_image_preview(self):
        if self.logo:
            return mark_safe(f'<img src = "{self.background_image.url}" width = "150" height="150"/> ')

    def save(self, *args, **kwargs):

        if not self.pk and Info.objects.exists():
            raise Info.ValidationError('There can be only one instance of Info')

        if self.pk:
            old_instance = Info.objects.get(pk=self.pk)
            self.change_image(old_instance, "background_image")
            self.change_image(old_instance, "logo")

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    def __str__(self):
        return self.cafe_title


class About(ImageMixin, models.Model):
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
            self.change_image(old_instance, "image")

        objects = About.objects.all()
        if objects:
            objects.update(is_active=False)
        self.is_active = True
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image:
            self.delete_image("image")

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title
