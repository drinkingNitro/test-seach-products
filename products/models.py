from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Name'))
    image = models.ImageField(verbose_name=_('Image'), upload_to='data/images')
    image_features = models.BinaryField(editable=False, null=True, verbose_name=_('Features'))


    def __str__(self):
        return self.name
