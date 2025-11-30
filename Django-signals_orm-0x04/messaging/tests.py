from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()

class MessageNotificationTest(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='pass')
        self.bob = User.objects.create_user(username='bob', password='pass')

    def test_notification_created_on_message(self):
        # no notifications initially
        self.assertEqual(Notification.objects.count(), 0)

        # alice sends a message to bob
        msg = Message.objects.create(sender=self.alice, receiver=self.bob, content='Hello Bob')

        # after message creation, a notification should exist for bob
        notifications = Notification.objects.filter(user=self.bob)
        self.assertEqual(notifications.count(), 1)

        n = notifications.first()
        self.assertEqual(n.actor, self.alice)
        self.assertEqual(n.message, msg)
        self.assertFalse(n.is_read)
        self.assertIn('sent you a message', n.verb)

