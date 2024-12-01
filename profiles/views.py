from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.http.response import HttpResponse
from django.core.paginator import Paginator

from .models import Profile
from .forms import UserForm, ProfileForm

from orders.models import Order


# Create your views here.
@method_decorator(login_required, name='dispatch')
class ProfileList(ListView):
    """
    Class ListView to display the items into a table.
    """

    paginate_by = 7
    model = Profile
    template_name = "profiles/profile_list.html"

    queryset = Profile.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProfileList, self).get_context_data(**kwargs)
        return context


@login_required
def customer_list(request):
    # Build query, users with account type 0 are customers
    queryset = Profile.objects.filter(account_type=0).all()
    queryset_two = Order.objects.values_list("profile", flat=True)
    queryset_three = Profile.objects.values_list("id", flat=True)
    # queryset_full = quert

    print(f"---1----{queryset}")
    print(f"---2----{queryset_two}")
    print(f"---3----{queryset_three}")
    # print(f"---UNI--- {query_union}")
    # 7 results per page
    customers = Paginator(queryset, 7)

    # Determine number of pages in query
    page_number = request.GET.get("page")
    page_obj = customers.get_page(page_number)

    return render(request, "customers/customer_list.html", {"page_obj": page_obj})


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

    # When form is submitted
    if request.method == "POST":

        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)

        # If both the user form and profile form are valid.
        if user_form.is_valid() and profile_form.is_valid():
            update_user = request.user
            #     This was the only definitive way of taking a model object
            # and updating it where the model was an inline relation to the
            # user AND allowed the user to update user fields themselves
            # (first_name, last_name, email) in conjunction to additional
            # profile details.
            # Individually referring to each object and updating it.

            # NB. Email should be readonly in the profile. If it is changed,
            # the email is no longer validated and can cause issues

            update_user.first_name = profile_form.data['first_name']
            update_user.last_name = profile_form.data['last_name']
            # Email is entered from the request.user, not the form post.
            update_user.email = request.user.email
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
            # Save the user
            update_user.save()

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
        'self_or_manage': "self",
        'user_form': user_form,
        'profile_form': profile_form,
    }

    # Render the view
    return render(request, template, context)


@login_required
def profile_manage(request, user_id):
    """
    Display another user's profile for management

    If no profile yet, create a new blank one to pair with a user.

    If one is found by its "user" (unique). Then it will load that
    data into the ProfileForm
    """

    get_user = get_object_or_404(User, id=user_id)

    # If the user uses url navigation to get to their own profile.
    # The template already changes the button for click function
    if get_user == request.user:
        return profile_view(request)

    else:
        profile, created = Profile.objects.get_or_create(
            user=get_user,
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
                update_user = get_user
                #     This was the only definitive way of taking a model object
                # and updating it where the model was an inline relation to the
                # user AND allowed the user to update user fields themselves
                # (first_name, last_name, email) in conjunction to additional
                # profile details.
                # Individually referring to each object and updating it.

                # Email should be readonly in the profile. If it is changed,
                # the email is no longer validated and can cause issues

                update_user.first_name = profile_form.data['first_name']
                update_user.last_name = profile_form.data['last_name']
                # Email is entered from the get_user, not the form post.
                update_user.email = get_user.email
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
                # Save the user
                update_user.save()

                # Display a message to the user to show it has worked
                messages.success(
                    request,
                    'Profile successfully updated'
                )

                return redirect('profile_manage', user_id=get_user.id)

            else:
                messages.error(
                    request, (
                        'Profile data is not valid.'
                        'Please check the validation prompts.'
                    )
                )

        else:
            # The query is a GET. Get the data to load into fields
            user_form = UserForm(instance=get_user)
            profile_form = ProfileForm(instance=profile)

        # Set template and context
        template = 'profiles/profile.html'
        context = {
            'user_id': get_user.id,
            'self_or_manage': "manage",
            'user_form': user_form,
            'profile_form': profile_form,
        }

        # Render the view
        return render(request, template, context)
