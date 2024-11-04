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
    user = request.user

    """
    If no profile yet, create a new blank one.

    If one is found by its "user" (unique). Then it will load that
    data into the Profile object instance
    """
    profile, created = Profile.objects.get_or_create(
        user=user,
        defaults={
            "account_type": 0,
            "address_line_1": "",
            "address_line_2": "",
            "address_line_3": "",
            "town": "",
            "county": "",
            "country": "GB",
            "postcode": "",
            "phone_number": ""
        },
    )

    # When form is submitted
    if request.method == "POST":
        user_form = UserForm(request.POST, prefix="user")
        profile_form = ProfileForm(request.POST, prefix="profile")

        # If both the user form and profile form are valid
        if user_form.is_valid() and profile_form.is_valid():

            profile = profile_form.save(commit=False)
            # profile.user = user
            #profile = get_object_or_404(Profile, user=user)
            #print("PROFILE")
            #print(profile)
            #print(profile_form)
            #profile = profile_form
            profile.user_id = user.id

            # Update the User object.
            user.first_name = request.POST['user-first_name']
            user.last_name = request.POST['user-last_name']
            user.email = request.POST['user-email']
            user.save()

            # Save the profile
            profile.save()
            messages.success(
                request,
                'Profile successfully updated'
            )
            print(messages)

            # return redirect(reverse('profile'))
    else:
        user_form = UserForm(instance=user, prefix="user")
        profile_form = ProfileForm(instance=profile, prefix="profile")

    template = 'profiles/profile.html'
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, template, context)
