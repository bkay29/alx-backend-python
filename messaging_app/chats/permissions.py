# chats/permissions.
from rest_framework import permissions  # Required 
from rest_framework.permissions import BasePermission


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission:
    - Allows only authenticated users
    - Allows access only if the user is a participant of the conversation
    """

    def has_permission(self, request, view):
        # Only authenticated users may access the API
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level restriction:
        - If obj is a Conversation → check participants
        - If obj is a Message → check obj.conversation.participants
        """
        # Conversation object
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # Message object
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        return False
