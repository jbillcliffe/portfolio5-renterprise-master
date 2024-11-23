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


class OrderForm(forms.Form):

    # Creating word variables to integer values
    AVAILABLE = 0
    SCRAPPED = 1
    MISSING = 2
    SOLD = 3
    REPAIR = 4

    # Creating tuples under the STATUS variable where an integer has a
    # relation to a string
    STATUS = (
        (AVAILABLE, 'Available'),
        (SCRAPPED, 'Scrapped'),
        (MISSING, 'Missing'),
        (SOLD, 'Sold'),
        (REPAIR, 'Repair')
    )

    class Meta:
        model = Order
        fields = '__all__'
        # fields = [
        #     'first_name', 'last_name', 'email', 'address_line_1',
        #     'address_line_2', 'address_line_3', 'town', 'county',
        #     'country', 'postcode', 'phone_number', 'delivery_date',
        #     'collect_date', 'status', 'category', 'item_type'
        # ]

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

        self.fields['delivery_date'] = (
            forms.DateField(widget=forms.TextInput(attrs={"type": "date"}))
        )

        self.fields['collect_date'] = (
            forms.DateField(widget=forms.TextInput(attrs={"type": "date"}))
        )

        self.fields['status'] = forms.ChoiceField(
            choices=self.STATUS, initial="",
            label="Status")

        all_types_and_cats = list(
            ItemType.objects.values('id', 'name', 'category'))
        all_types = [('', '--- Please Select ---')]
        all_categories = [('', '--- Please Select ---')]
        counter = 0

        for x in all_types_and_cats:
            id_cat_string = (
                f"{x["id"]}|"
                f"{x["category"]}"
            )
            all_types.append(
                (id_cat_string, x["name"])
            )

            if (any(x["category"] in i for i in all_categories)):
                # Do not duplicate the entry
                pass
            else:
                all_categories.append(
                    (counter, x["category"])
                )
                counter += 1

        self.fields['category'] = forms.ChoiceField(
            choices=all_categories, label="Category")
        self.fields['item_type'] = forms.ChoiceField(
            choices=all_types, label="Item Type")

        self.helper = FormHelper(self)
        self.helper.attrs['autocomplete'] = 'off'
        self.helper.form_tag = False
        self.fields["item_type"].widget.attrs["disabled"] = True
        self.helper.layout = Layout(
            BS5Accordion(
                AccordionGroup(
                    "Customer",
                    FloatingField("first_name", wrapper_class="col-12 p-0"),
                    FloatingField("last_name", wrapper_class="col-12 p-0"),
                    FloatingField("email", wrapper_class="col-12 p-0"),
                    FloatingField("phone_number", wrapper_class="col-12 p-0")
                ),
                AccordionGroup(
                    "Address",
                    FloatingField(
                        "address_line_1", wrapper_class="col-12 p-0"),
                    FloatingField(
                        "address_line_2", wrapper_class="col-12 p-0"),
                    FloatingField(
                        "address_line_3", wrapper_class="col-12 p-0"),
                    FloatingField("town", wrapper_class="col-12 p-0"),
                    FloatingField("county", wrapper_class="col-12 p-0"),
                    FloatingField("country", wrapper_class="col-12 p-0"),
                    FloatingField("postcode", wrapper_class="col-12 p-0")
                ),
                AccordionGroup(
                    'Order',
                    FloatingField(
                        'category',
                        wrapper_class='col-12 p-0',
                        onchange='getCreateOrderItemTypes()'),
                    FloatingField(
                        'item_type',
                        onchange="validateDates()",
                        wrapper_class='col-12 p-0'),
                    FloatingField(
                        'delivery_date',
                        onchange='validateDates()',
                        wrapper_class='col-12 p-0'),
                    FloatingField(
                        'collect_date',
                        onchange='validateDates()',
                        wrapper_class='col-12 p-0'),
                ),
                flush=True,
                always_open=False,
            ),
        )

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
