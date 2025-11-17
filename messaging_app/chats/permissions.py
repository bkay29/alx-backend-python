# chats/permissions.py
from rest_framework.permissions import BasePermission

class IsConversationParticipant(BasePermission):
    """
    Allow access only to users who are part of the conversation.

    This permission works for both Conversation and Message objects:
    - If obj has `participants` (Conversation), it checks if request.user is in participants.
    - If obj has `conversation` (Message), it checks if request.user is in the message's conversation participants.
    """

    def has_object_permission(self, request, view, obj):
        # Conversation object
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        # Message object
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        return False
