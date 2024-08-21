from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Name'))
    image = models.ImageField(verbose_name=_('Image'), upload_to='product_images')
    features = models.ManyToManyField(to='ImageFeature', verbose_name=_('Features'), related_name='products')


    def __str__(self):
        return self.name


class ImageFeature(models.Model):
    feature = models.CharField(max_length=100, unique=True, verbose_name=_('Feature'))

    def __str__(self):
            return self.feature
