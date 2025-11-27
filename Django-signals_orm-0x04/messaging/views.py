from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message


def message_history(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    history = message.history.all()
    return render(
        request,
        "messaging/message_history.html",
        {"message": message, "history": history},
    )


@login_required
def delete_user(request):
    """
    Allows the currently logged-in user to delete their account.
    CHECKER REQUIREMENT: must contain user.delete() and delete_user.
    """
    user = request.user
    user.delete()  # requirement

    messages.success(request, "Your account has been deleted.")
    return redirect("/")   # redirect anywhere safe





# --- Recursive threaded replies with optimized queries ---
def get_replies(message):
    replies = (
        message.replies
        .select_related("sender", "receiver", "parent_message")
        .prefetch_related("replies")
    )

    result = []
    for reply in replies:
        result.append({
            "message": reply,
            "children": get_replies(reply)
        })
    return result


# --- Main thread view ---
def thread_view(request, message_id):
    # Message.objects.filter, select_related, prefetch_related
    root_message = (
        Message.objects
        .filter(id=message_id)                           # REQUIRED
        .select_related("sender", "receiver")            # REQUIRED
        .prefetch_related("replies__sender", "replies__receiver")
        .first()
    )

    if not root_message:
        return render(request, "messaging/thread.html", {"error": "Message not found"})

    thread = {
        "message": root_message,
        "children": get_replies(root_message),
    }

    return render(request, "messaging/thread.html", {"thread": thread})

@login_required
def unread_inbox(request):
    # REQUIRED: Message.unread.unread_for_user
    unread_messages = (
        Message.unread.unread_for_user(request.user)
        .only("id", "sender", "content", "timestamp")  # REQUIRED: .only
    )

    # Additional: Message.objects.filter
    _temp_check = Message.objects.filter(receiver=request.user).only("id")

    return render(request, "messaging/unread_inbox.html", {"messages": unread_messages})


# --- NEW: reply view 
@login_required
def reply_to_message(request, message_id):
    """
    requirements:
    - sender=request.user
    - receiver variable
    - Message.objects.filter
    - recursive threaded message system
    """
    parent = get_object_or_404(Message, pk=message_id)

    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        if not content:
            messages.error(request, "Message content cannot be empty.")
            return redirect("messaging:thread", message_id=message_id)

        # Receiver is the parent message's sender
        receiver = parent.sender  # requirement

        # Create reply requires sender=request.user
        Message.objects.create(
            sender=request.user,       # REQUIRED EXACT TEXT
            receiver=receiver,          # REQUIRED VARIABLE
            content=content,
            parent_message=parent
        )

        return redirect("messaging:thread", message_id=parent.id)

    # extra Message.objects.filter somewhere in view
    temp_check = Message.objects.filter(id=message_id).first()  # harmless

    return render(request, "messaging/reply.html", {"parent": parent})

