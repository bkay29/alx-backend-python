# chats/permissions.py
from rest_framework import permissions  # Required 
from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission:
    - Allows only authenticated users
    - Allows access only if the user is a participant of the conversation
    - Explicitly checks for PUT / PATCH / DELETE to enforce participant-only edits
    """

    def has_permission(self, request, view):
        # Only authenticated users may access the API
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level restriction:
        - If obj is a Conversation -> check participants
        - If obj is a Message -> check obj.conversation.participants
        Also explicitly consider HTTP methods for create/update/delete.
        """

        # Normalize participant check
        def is_participant(user, conversation_obj):
            return user in conversation_obj.participants.all()

        # Conversation object
        if hasattr(obj, "participants"):
            # read actions (GET) require being a participant
            if request.method in ("GET", "HEAD", "OPTIONS"):
                return is_participant(request.user, obj)

            # write actions (PUT, PATCH, DELETE) must also be participants
            if request.method in ("PUT", "PATCH", "DELETE", "POST"):
                return is_participant(request.user, obj)

            # default deny
            return False

        # Message object
        if hasattr(obj, "conversation"):
            conv = obj.conversation

            # read actions
            if request.method in ("GET", "HEAD", "OPTIONS"):
                return is_participant(request.user, conv)

            # write/update/delete actions
            if request.method in ("PUT", "PATCH", "DELETE", "POST"):
                return is_participant(request.user, conv)

            return False

        return False
