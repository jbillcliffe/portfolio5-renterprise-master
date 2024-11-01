from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import ProfileForm


# Create your views here.
@login_required
def profile(request):
    """
    Display Profile
    """
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == "post":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Form is not valid')
    else:

        form = ProfileForm(instance=profile)
    template = 'profiles/profile.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
