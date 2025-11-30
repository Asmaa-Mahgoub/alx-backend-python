from django.db import models

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Return unread messages for a specific user.
        Only fetch id, content, and timestamp for optimization.
        """
        return self.filter(receiver=user, read=False).only('id', 'content', 'timestamp')
    
