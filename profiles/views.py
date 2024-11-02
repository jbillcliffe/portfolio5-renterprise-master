from django.contrib.auth.admin import User
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import UserForm, ProfileForm


# Create your views here.
@login_required
def profile(request):
    """
    Display Profile
    """
    profile = get_object_or_404(Profile, user=request.user)
    user = request.user

    # if request.method == "post":

    # if form.is_valid():
    #    form.save()
    #    messages.success(request, 'Profile updated successfully')
    # else:
    #    messages.error(request, 'Update failed. Form is not valid')
    # else:
    if request.method == "POST":
        # Do some validating and saving
        user_form = UserForm(request.POST, prefix="user")
        profile_form = ProfileForm(request.POST, prefix="profile")

        if user_form.is_valid() and profile_form.is_valid():

            profile = profile_form.save(commit=False)

            try:
                user_object = User.objects.get(request.user)
                user_object.first_name = user_form.first_name
                user_object.last_name = user_form.last_name
                user_object.email = user_form.email
                user_object.save()
            except User.DoesNotExist:
                messages.add_message(
                    request, messages.ERROR,
                    'User Account Does Not Exist!'
                )
            print(messages)

            return redirect(reverse('profile'))
    else:

        user_form = UserForm(instance=user, prefix="user")
        profile_form = ProfileForm(instance=profile, prefix="profile")

    template = 'profiles/profile.html'
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, template, context)
