# messaging/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance: Message, created, **kwargs):
    """
    When a new Message is created, create a Notification for the receiver.
    """
    if not created:
        return

    # avoid notifying the sender when they send to themselves (optional)
    if instance.sender == instance.receiver:
        return

    Notification.objects.create(
        user=instance.receiver,
        actor=instance.sender,
        message=instance,
        verb=f"{instance.sender.get_full_name() or instance.sender.username} sent you a message"
    )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance: Message, **kwargs):
    """
    Before saving a Message, if this is an update and content changed,
    save the old content into MessageHistory, and update edited flags.
    """

    # If instance is new (being created), nothing to log
    if instance._state.adding:
        return

    try:
        # fetch current persisted record
        old = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        # no previous record found — treat as new
        return

    # If content did not change, don't log
    if old.content == instance.content:
        return

    # Determine editor if caller supplied it. (See below for how to set instance._editor)
    editor = getattr(instance, '_editor', None)

    # Create the history record with the old content
    MessageHistory.objects.create(
        message=old,
        old_content=old.content,
        editor=editor
    )

    # Update the Message's edited metadata (use timezone.now for consistent tz-aware timestamps)
    instance.edited = True
    instance.last_edited_at = timezone.now()
    if editor:
        instance.last_edited_by = editor