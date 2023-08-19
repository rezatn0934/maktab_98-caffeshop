from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe

from utils import phoneNumberRegex, ImageMixin


# Create your models here.


class Gallery(ImageMixin, models.Model):
    title = models.CharField(verbose_name=_("Image Title"), max_length=50)
    is_active = models.BooleanField(verbose_name=_("Active"), default=True)
    image = models.ImageField(verbose_name=_("Image"), upload_to='images/gallery')

    class Meta:
        verbose_name_plural = "Gallery"

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
    cafe_title = models.CharField(verbose_name=_("Cafe Title"), max_length=25)
    cafe_motto = models.TextField(verbose_name=_("Cafe Motto"), )
    phone = models.CharField(verbose_name=_("Phone Number"), validators=[phoneNumberRegex])
    email = models.EmailField(verbose_name=_("Email Address"), )
    work_hours = models.CharField(verbose_name=_("Working Hours"), max_length=100)
    address = models.TextField(verbose_name=_("Address"), )
    instagram = models.URLField(verbose_name=_("Instagram Link"), )
    facebook = models.URLField(verbose_name=_("Facebook Link"), )
    twitter = models.URLField(verbose_name=_("Twitter Link"), )
    background_image = models.ImageField(verbose_name=_("Background Image"), upload_to='images/HomePageBackground')
    logo = models.ImageField(verbose_name=_("Logo"), upload_to='images/logo', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Info"

    def logo_preview(self):
        if self.logo:
            return mark_safe(f'<img src = "{self.logo.url}" width = "50" height="80"/> ')

    def background_image_preview(self):
        if self.background_image:
            return mark_safe(f'<img src = "{self.background_image.url}" width = "150" height="150"/> ')

    def save(self, *args, **kwargs):

        if not Info.objects.exists():
            super().save(*args, **kwargs)
        else:
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
    title = models.CharField(verbose_name=_("About Us Title"), max_length=30)
    content = models.TextField(verbose_name=_("About Us Content"))
    is_active = models.BooleanField(verbose_name=_("Active"), default=True)
    image = models.ImageField(verbose_name=_("About Us Image"), upload_to='images/about')

    class Meta:
        verbose_name_plural = "About"

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
