from django import forms
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_bootstrap5.bootstrap5 import FloatingField

from .models import Profile

"""
Creating a UserForm & Profile Form. 
These merge into the overall profile form on post.
eg. User Field : profile.user.first_name
    Profile Field : profile.address_line_1
Using FloatingFields as this feature from Bootstrap 5 is an excellent
use of the space provided for clear requirement and then clearly
showing input after typing
"""


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.attrs['autocomplete'] = 'off'
        self.helper.form_tag = False
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        # To prevent editing email visually.
        # views.py handles any other attempts by not using any
        # email value from the post.
        self.fields['email'].widget.attrs['readonly'] = True

        self.helper.layout = Layout(
            FloatingField("first_name"),
            FloatingField("last_name"),
            FloatingField("email"),
        )


class ProfileForm(forms.ModelForm):

    # Exclude the user value, this will be handled in views.py
    class Meta:
        model = Profile
        exclude = ('user', )

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.attrs['autocomplete'] = 'off'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            FloatingField("account_type"),
            FloatingField("address_line_1"),
            FloatingField("address_line_2"),
            FloatingField("address_line_3"),
            FloatingField("town"),
            FloatingField("county"),
            FloatingField("country"),
            FloatingField("postcode"),
            FloatingField("phone_number")
        )
