from django.shortcuts import render, get_object_or_404
from .models import Message

def message_history(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    history = message.history.all()
    return render(request, "messaging/message_history.html", {"message": message, "history": history})
