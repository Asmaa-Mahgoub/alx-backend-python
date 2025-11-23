from rest_framework import permissions

class IsParticipant(permissions.BasePermission):
    """
    Allow access only to conversation participants.
    """

    def has_permission(self, request, view):
        # Global check: Must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False  # DRF will return HTTP_403_FORBIDDEN
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        # obj could be Conversation
        if hasattr(obj, 'participants'):
            return obj.participants.filter(pk=user.pk).exists()

        # obj could be Message → check its conversation participants
        if hasattr(obj, 'conversation'):
            return obj.conversation.participants.filter(pk=user.pk).exists()

        return False
