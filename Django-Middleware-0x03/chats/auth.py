# chats/auth.py
from rest_framework.permissions import BasePermission

class IsConversationParticipant(BasePermission):
    """
    Allow access only to users who are part of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        # obj can be Conversation or Message
        if hasattr(obj, 'participants'):  # conversation
            return request.user in obj.participants.all()

        if hasattr(obj, 'conversation'):  # message
            return request.user in obj.conversation.participants.all()

        return False
