from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification


class MessagingTests(TestCase):
    def test_message_creation(self):
        u1 = User.objects.create(username="alice")
        u2 = User.objects.create(username="bob")

        msg = Message.objects.create(sender=u1, receiver=u2, content="Hello")
        self.assertIsNotNone(msg.id)

