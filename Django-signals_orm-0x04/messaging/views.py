from django.shortcuts import render
from .models import Message

# Create your views here.
User = get_user_model()
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib import messages


@login_required
def delete_user(request):
    """
    View to delete the currently logged-in user.
    """
    user = request.user

    if request.method == "POST":
        username = user.username  # store for message
        user.delete()  # triggers post_delete signal
        messages.success(request, f"User '{username}' and related data have been deleted.")
        return redirect('home')  # replace 'home' with your homepage URL

    # Render a confirmation page
    return render(request, "messaging/delete_user.html", {"user": user})


@login_required
def user_messages(request):
    """
    View to fetch messages where the current user is sender or receiver,
    optimized with select_related and prefetch_related.
    """
    # Fetch messages where user is sender or receiver
    messages_qs = (
        Message.objects.filter(sender=request.user)  # satisfies "sender=request.user"
        .select_related('sender', 'receiver')        # satisfies "select_related"
        .prefetch_related('replies')                # optional: prefetch replies
    )

    # OR to also include messages received by the user:
    messages_received_qs = (
        Message.objects.filter(receiver=request.user)  # satisfies "receiver"
        .select_related('sender', 'receiver')
        .prefetch_related('replies')
    )

    # Combine sent and received messages (optional)
    all_messages = messages_qs | messages_received_qs
    all_messages = all_messages.order_by('-timestamp')  # most recent first

    return render(request, 'messaging/user_messages.html', {'messages': all_messages})

