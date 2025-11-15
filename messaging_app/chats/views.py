# chats/views.py
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer

# --------- CONVERSATION VIEWSET ---------
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Custom action to create a new conversation
    def create(self, request, *args, **kwargs):
        participants_ids = request.data.get('participants', [])
        if len(participants_ids) < 2:
            return Response({"error": "A conversation must have at least 2 participants."}, status=400)
        conversation = Conversation.objects.create()
        conversation.participants.set(User.objects.filter(user_id__in=participants_ids))
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=201)

# --------- MESSAGE VIEWSET ---------
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Override create to send message to existing conversation
    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation')
        sender_id = request.data.get('sender')
        message_body = request.data.get('message_body')

        if not all([conversation_id, sender_id, message_body]):
            return Response({"error": "conversation, sender, and message_body are required."}, status=400)

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
            sender = User.objects.get(user_id=sender_id)
        except (Conversation.DoesNotExist, User.DoesNotExist):
            return Response({"error": "Invalid conversation or sender."}, status=404)

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=201)
