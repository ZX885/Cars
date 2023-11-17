from django.db import models
from math import exp
import os
from datetime import datetime
from django.conf import settings
from django.db.models.signals import post_save
from django.db import IntegrityError, models
from django.contrib.auth.models import User
from PIL import Image
from django.dispatch import receiver


# Create your models here.




class CarsManager(models.Manager):
    pass


class NullPriceException(Exception):
    pass


class Cars(models.Model):
    title: str = models.CharField(max_length=50)
    description: str = models.TextField()
    author: User = models.ForeignKey(User, on_delete=models.SET_NULL,
                                     null=True, blank=True)
    type: str = models.CharField(max_length=25, null=True, blank=True)
    is_available: bool = models.BooleanField(default=True)
    price: float = models.DecimalField(max_digits=9, decimal_places=1)
    created: datetime = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        default='static/img/bmw_def.jpg', upload_to="static/img")

    objects = models.Manager()  # default
    c_objects = CarsManager()  # custom manager

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.type == None or self.type == "":
            raise IntegrityError("Type cannot be null")
        if self.price == 0:
            raise NullPriceException
        super().save(*args, **kwargs)

        # We have to save the form first before getting the image path
        img = Image.open(self.image.path)
        if img.height > 600 or img.width > 600:
            output_size = (600, 600)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def delete(self, *args, **kwargs):
        image_url = self.image.url
        if image_url != 'static/img/bmw_def.jpg':
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['is_available', 'price']),
        ]
# @receiver(post_save, sender=Cars)
# def print_info_of_cars(sender, instance, created, **kwatgs):
#     if created:
#         print("----------------------------------------------------")
#         print(f"Cars instance named: {instance.title} was created")
#         print("----------------------------------------------------")
       
#     else:
#         print("------------------------------------------------")
#         print("Error while sending car: ")
#         print("------------------------------------------------")