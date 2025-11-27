from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.models import User

from .models import Message, Notification


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        # Use filter() chaining instead of get()
        receiver_user = User.objects.filter(id=instance.receiver.id).first()
        if receiver_user is None:
            return

        Notification.objects.create(
            user=receiver_user,
            message=instance
        )

    except (ObjectDoesNotExist, MultipleObjectsReturned):
        # Avoid breaking signal chain
        pass
