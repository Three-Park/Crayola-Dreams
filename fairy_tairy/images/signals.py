from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Image

@receiver(post_save, sender=Image)
def update_image_url(sender, instance, **kwargs):
    if instance.image:
        instance.image_url = instance.image.url
        instance.save(update_fields=['image_url'])