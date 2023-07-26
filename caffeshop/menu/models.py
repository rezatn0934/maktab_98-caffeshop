from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    image = models.ImageField(upload_to='images/category/', blank=True, null=True)

    def __str__(self):
        return self.name

