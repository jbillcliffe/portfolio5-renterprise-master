from django import forms
from django.db import models
# from django.forms import inlineformset_factory
# from django.shortcuts import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Reset, Submit, Field
from crispy_forms.bootstrap import StrictButton, AccordionGroup
from crispy_bootstrap5.bootstrap5 import BS5Accordion, FloatingField, Switch

from django_countries.fields import CountryField
from localflavor.gb.gb_regions import GB_REGION_CHOICES

from .models import Order
# from profiles.models import Profile, User
# from profiles.forms import ProfileForm, UserForm
from items.models import Item, ItemType


# class InlineOrderItemForm(forms.ModelForm):

#     class Meta:
#         model = Item
#         fields = '__all__'

#     def __init__(self, data=None, files=None,
#                  auto_id='id_%s', prefix=None, queryset=None,
#                  *args, **kwargs):

#         # initial = kwargs.get('initial', {})
#         # initial['item_type'] = Item()
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.attrs['autocomplete'] = 'off'
#         self.helper.form_tag = False

#         self.helper.layout = (
#             Field('delivery_date', type="hidden", id="id_status"),
#             Field('collect_date', type="hidden", id="id_status"),
#             Field('repair_date', type="hidden", id="id_status"),
#             Field('status', type="hidden", id="id_status")
#         )


# class InlineOrderProfileForm(forms.ModelForm):

#     class Meta:
#         model = Profile
#         exclude = ('user', )

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.helper = FormHelper(self)
#         self.helper.attrs['autocomplete'] = 'off'
#         self.helper.form_tag = False
#         self.helper.layout = Layout(
#             FloatingField("phone_number"),
#             FloatingField("account_type"),
#             FloatingField("address_line_1"),
#             FloatingField("address_line_2"),
#             FloatingField("address_line_3"),
#             FloatingField("town"),
#             FloatingField("county"),
#             FloatingField("country"),
#             FloatingField("postcode")
#         )


class OrderForm(forms.Form):

    # item_type = forms.ForeignKey(
    #     ItemType, on_delete=models.CASCADE, related_name="item_type",
    #     label="Item Type")

    class Meta:
        model = Order
        exclude = ('created_on', 'created_by',)

    def __init__(self, *args, **kwargs):

        super(OrderForm, self).__init__(*args, **kwargs)

        self.fields['first_name'] = forms.CharField(
            max_length=30, required=True, initial="",
            label="First Name")

        self.fields['last_name'] = forms.CharField(
                max_length=50, required=True, initial="",
                label="Last Name")

        self.fields['email'] = forms.EmailField(
                max_length=100, required=True, initial="",
                label="Email Address")

        self.fields['address_line_1'] = forms.CharField(
                max_length=80, required=True, initial="",
                label="First Line of Address")

        self.fields['address_line_2'] = forms.CharField(
                max_length=80, required=False, initial="",
                label="Second Line of Address")

        self.fields['address_line_3'] = forms.CharField(
                max_length=80, required=False, initial="",
                label="Third Line of Address")

        self.fields['town'] = forms.CharField(
                max_length=40, required=True, initial="",
                label="Town/City")

        self.fields['county'] = forms.ChoiceField(
                choices=GB_REGION_CHOICES, initial="",
                label="County")

        self.fields['country'] = CountryField(
            blank_label='Select country', default="GB"
        ).formfield()

        self.fields['postcode'] = forms.CharField(
                max_length=20, required=True, initial="",
                label="Postcode")

        self.fields['phone_number'] = forms.CharField(
                max_length=40, required=True, initial="",
                label="Phone Number")

        item_types = ItemType.objects.all()
        categories = (
            item_types.order_by("category")
            .distinct("category").values("category"))
        print(categories)

        # self.fields['category'] = forms.ModelChoiceField(
        #     )

        self.fields['item_type'] = forms.ModelChoiceField(
            queryset=ItemType.objects.all())

        

        # User
        # Profile
        # Item

        # User
        # fields = ['first_name', 'last_name', 'email']

        self.helper = FormHelper(self)
        self.helper.attrs['autocomplete'] = 'off'
        self.helper.form_tag = False
        # self.helper.layout = Layout()

        #         HTML(
        #             '{% with status_array=template_status %}'
        #             '{% for x, y in status_array %}'
        #             # Create a div at each one.
        #             '<div class="form-check form-switch mb-3">'
        #             '<input'
        #             ' class="form-check-input {{ x }} me-3"'
        #             ' type="checkbox" role="switch"'
        #             ' onchange="statusSwitchChanger(\'{{ x }}\')"'
        #             ' value={{ forloop.counter0 }}'
        #             ' id="id-status-{{ x }}">'
        #             '<label class="form-check-label"'
        #             ' for="id-status-{{ x }}">'
        #             '{{ y }}</label>'
        #             '</div>'
        #             '{% endfor %}'
        #             '{% endwith %}'
        #         ),
        #         Field('status', type="hidden", id="id_status"),
        #         HTML(
        #             '<input name="status-item_id"'
        #             ' id="id_status_id" value="{{ item_id }}" hidden>'),
        #         # Submit("status-submit", "Submit"),
        #         Div(
        #             # Submit means this defaults to performing the
        #             # "form action"
        #             Submit(
        #                 'submit-status-edit', 'Update Status',
        #                 css_id='edit-status-submit-button',
        #                 css_class='default-button mb-2'
        #             ),
        #             # Returns the form to it's original state.
        #             # Removing "editing" status field, making sure the type
        #             # dropdown isn't disabled, resetting the image display
        #             # and image text area are done in JS
        #             Reset(
        #                 'cancel-status-edit', 'Cancel',
        #                 css_id='edit-status-cancel-button',
        #                 css_class='danger-button',
        #                 data_bs_dismiss='modal'),
        #             css_class="row modal-footer justify-content-center pb-0"
        #         ),
        #         css_id="item-status-change-modal",
        #         css_class="modal-sm",
        #         title="Set Item Status"
        #     )
        # )
