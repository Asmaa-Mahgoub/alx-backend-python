from django.shortcuts import render

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

