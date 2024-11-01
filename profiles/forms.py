from django import forms
from .models import Profile


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
        placeholders = {
            'account_type': 'Account Type',
            'address_line_1': 'First Line of Address',
            'address_line_2': 'Second Line of Address',
            'address_line_3': 'Third Line of Address',
            'town': 'Town or City',
            'county': 'County',
            'postcode': 'Postcode',
            'phone_number': 'Phone Number',
        }

        self.fields['address_line_1'].widget.attrs['autofocus'] = True

        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            # self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
            self.fields[field].label = False
