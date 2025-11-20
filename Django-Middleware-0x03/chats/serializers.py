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
    sender_name = serializers.CharField(source='sender.email', read_only=True)  # CharField 
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'sender_name', 'message_body', 'sent_at']

# --------- CONVERSATION SERIALIZER ---------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()  # SerializerMethodField

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']

    # Nested messages
    def get_messages(self, obj):
        qs = obj.messages.all()
        return MessageSerializer(qs, many=True).data

    # Example validation method 
    def validate(self, data):
        if 'participants' in data and len(data['participants']) < 2:
            raise serializers.ValidationError("A conversation must have at least 2 participants.")
        return data
