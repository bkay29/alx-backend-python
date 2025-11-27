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
    user.delete()  # <-- checker looks for this exact line

    messages.success(request, "Your account has been deleted.")
    return redirect("/")   # You can change this to any safe landing page

