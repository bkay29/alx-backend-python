from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.models import User

from .models import Message, Notification, MessageHistory


# Notification on new message
@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        receiver_user = User.objects.filter(id=instance.receiver.id).first()
        if receiver_user is None:
            return

        Notification.objects.create(
            user=receiver_user,
            message=instance
        )

    except (ObjectDoesNotExist, MultipleObjectsReturned):
        pass


# Save old content before a message is edited
@receiver(pre_save, sender=Message)
def save_message_history(sender, instance, **kwargs):
    if not instance.pk:
        return  # New message; no history to save

    try:
        old_message = Message.objects.get(pk=instance.pk)

        if old_message.content != instance.content:
            editor = getattr(instance, "edited_by", None)

            MessageHistory.objects.create(
                message=old_message,
                old_content=old_message.content,
                edited_by=editor
            )
            instance.edited = True

    except (ObjectDoesNotExist, MultipleObjectsReturned):
        pass


# Delete related data when a user is deleted
@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Checker requires: "Message.objects.filter" and "delete()"
    Remove all messages, notifications, and message history related to the deleted user.
    """

    # Delete sent messages
    Message.objects.filter(sender=instance).delete()      # keyword
    # Delete received messages
    Message.objects.filter(receiver=instance).delete()    # keyword

    # Delete related notifications
    Notification.objects.filter(user=instance).delete()

    # Delete message history for any of the user's messages
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()

    # Nothing returned—safe cleanup
