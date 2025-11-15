# chats/serializers.py
from rest_framework import serializers
from .models import User, Conversation, Message

# --------- USER SERIALIZER ---------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']

# --------- MESSAGE SERIALIZER ---------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Nested sender info

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at']

# --------- CONVERSATION SERIALIZER ---------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)  # Nested participants
    messages = MessageSerializer(many=True, read_only=True)   # Nested messages

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
