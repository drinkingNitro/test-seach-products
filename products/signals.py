from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Product
from .utils.image_features import extract_features


@receiver(post_save, sender=Product)
def save_image_features(sender, instance, **kwargs):
    if instance.image:
        image_path = instance.image.path
        features = extract_features(image_path)
        instance.image_features = features.tobytes()
        instance.save()
