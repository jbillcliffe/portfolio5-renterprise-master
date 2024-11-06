from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import UserForm, ProfileForm


# Create your views here.
@login_required
def profile_view(request):
    """
    Display Profile

    If no profile yet, create a new blank one to pair with a user.

    If one is found by its "user" (unique). Then it will load that
    data into the ProfileForm
    """

    profile, created = Profile.objects.get_or_create(
        user=request.user,
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
# Fix user not updating incoming
    # When form is submitted
    if request.method == "POST":

        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)

        # If both the user form and profile form are valid.
        if user_form.is_valid() and profile_form.is_valid():

            #     This was the only definitive way of taking a model object
            # and updating it where the model was an inline relation to the
            # user AND allowed the user to update user fields themselves
            # (first_name, last_name, email) in conjunction to additional
            # profile details.
            # Individually referring to each object and updating it.

            # NB. Email should be readonly in the profile. If it is changed,
            # the email is no longer validated and can cause issues

            profile.user.first_name = profile_form.data['first_name']
            profile.user.last_name = profile_form.data['last_name']
            # Email is entered from the request.user, not the form post.
            profile.user.email = request.user.email
            profile.address_line_1 = profile_form.data['address_line_1']
            profile.address_line_2 = profile_form.data['address_line_2']
            profile.address_line_3 = profile_form.data['address_line_3']
            profile.town = profile_form.data['town']
            profile.county = profile_form.data['county']
            profile.country = profile_form.data['country']
            profile.postcode = profile_form.data['postcode']
            profile.phone_number = profile_form.data['phone_number']

            # Save the profile
            profile.save()

            # Display a message to the user to show it has worked
            messages.success(
                request,
                'Profile successfully updated'
            )

            return redirect(reverse('profile_view'))

        else:
            messages.error(
                request, (
                    'Profile data is not valid.'
                    'Please check the validation prompts.'
                )
            )

    else:
        # The query is a GET. Get the data to load into fields
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    # Set template and context
    template = 'profiles/profile.html'
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    # Render the view
    return render(request, template, context)
