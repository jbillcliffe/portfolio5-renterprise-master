from django import forms
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_bootstrap5.bootstrap5 import FloatingField

from .models import Profile


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

        self.helper.layout = Layout(
            FloatingField("first_name"),
            FloatingField("last_name"),
            FloatingField("email"),
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.attrs['autocomplete'] = 'off'
        self.helper.form_tag = False
        # self.helper.attrs['autocomplete'] = 'off'
        # self.helper.attrs['label']
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

