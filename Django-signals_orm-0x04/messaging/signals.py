from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.models import User

from .models import Message, Notification, MessageHistory

# notification on new message
@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        # Use .filter instead of .get to avoid exceptions
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
    If content has changed, store previous version in MessageHistory,
    including who edited it if available.
    """
    # Skip new messages (no history to log)
    if not instance.pk:
        return

    try:
        old_message = Message.objects.get(pk=instance.pk)

        # Only create history if content changed
        if old_message.content != instance.content:
            # Capture the editor if set (views can assign instance.edited_by = request.user)
            editor = getattr(instance, "edited_by", None)

            MessageHistory.objects.create(
                message=old_message,
                old_content=old_message.content,
                edited_by=editor
            )
            instance.edited = True

    except (ObjectDoesNotExist, MultipleObjectsReturned):
        pass
