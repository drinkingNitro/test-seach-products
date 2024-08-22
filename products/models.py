from django.db import models
from django.utils.translation import gettext_lazy as _

from django.db.models.signals import post_save
from django.dispatch import receiver
import numpy as np

from .utils.image_features import extract_features

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Name'))
    image = models.ImageField(verbose_name=_('Image'), upload_to='data/images')
    image_features = models.BinaryField(editable=False, null=True, verbose_name=_('Features'))


    def __str__(self):
        return self.name


@receiver(post_save, sender=Product)
def save_image_features(sender, instance, **kwargs):
    if instance.image:
        image_path = instance.image.path
        features = extract_features(image_path)
        instance.image_features = features.tobytes()
        instance.save()
