from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.models import User

from .models import Message, Notification

# notification on new message
@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        # Use . filter instead of . get to avoid exceptions
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

# save message history before edit
@receiver(pre_save, sender=Message)
def save_message_history(sender, instance, **kwargs):
    """
    Trigger BEFORE a Message is saved.
    If content has changed, store old version in MessageHistory.
    """

    # If it's a NEW object, skip (no history to log)
    if not instance.pk:
        return

    try:
        old_message = Message.objects.get(pk=instance.pk)

        # Only create history if content changed
        if old_message.content != instance.content:
            MessageHistory.objects.create(
                message=old_message,
                old_content=old_message.content
            )
            instance.edited = True

    except (ObjectDoesNotExist, MultipleObjectsReturned):
        pass    
