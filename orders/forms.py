from django import forms
from django.db import models

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Reset, Submit, Field
from crispy_forms.bootstrap import AccordionGroup, StrictButton  # , TabHolder, Tab
from crispy_bootstrap5.bootstrap5 import BS5Accordion, FloatingField

from django_countries.fields import CountryField
from localflavor.gb.gb_regions import GB_REGION_CHOICES

from .models import Order
# from profiles.models import Profile, User
# from profiles.forms import ProfileForm, UserForm
from items.models import ItemType, Item


# class OrderViewForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['start_date', 'end_date']

#         # Order(*, profile, item, cost_initial, cost_week, start_date, end_date, created_on, created_by)
#         # Invoice(*, created_on, created_by, order, note, due_on, amount_paid, status, stripe_pid)
#         
#         # ItemType(*, name, sku, category, cost_initial, cost_week, meta_tags, product_stripe_id)
#         # Profile(*, user, account_type, address_line_1, address_line_2, address_line_3, town, county, postcode, phone_number, stripe_id)

#     def __init__(self, *args, **kwargs):
#         """
#         Add placeholders and classes, remove auto-generated
#         labels and set autofocus on first field
#         """
#         super().__init__(*args, **kwargs)


class OrderDatesForm(forms.ModelForm):
    # Order(*, start_date, end_date)
    class Meta:
        model = Order
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.TextInput(
                attrs={
                    'type': 'date',
                    'onchange': 'validateDates();'
                }
            ),
            'end_date': forms.TextInput(
                attrs={
                    'type': 'date',
                    'onchange': 'validateDates();'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.attrs['autocomplete'] = 'off'


class OrderItemForm(forms.ModelForm):
    # Item(*, item_type, item_serial, repair_date, status)
    class Meta:
        model = Item
        fields = ['id', 'item_type', 'item_serial', 'repair_date', 'status']
        labels = {
            "item_type": "Type",
            "item_serial": "Serial No.",
            "repair_date": "Logged Repair Date",
            "item_status": "Item Status",
        }

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.attrs['autocomplete'] = 'off'


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

    def __init__(self, *args, **kwargs):

        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['profile'] = forms.IntegerField()
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

        self.fields['start_date'] = (
            forms.DateField(widget=forms.TextInput(attrs={"type": "date"}))
        )

        self.fields['end_date'] = (
            forms.DateField(widget=forms.TextInput(attrs={"type": "date"}))
        )

        self.fields['cost_initial'] = (
            forms.DecimalField(max_digits=6, decimal_places=2)
        )
        self.fields['cost_week'] = (
            forms.DecimalField(max_digits=6, decimal_places=2)
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
        self.fields['item'] = forms.IntegerField()
        self.fields['invoice_notes'] = forms.CharField(
            required=False,
            widget=forms.Textarea(
                attrs={
                    "rows": "4"
                })
        )

        self.helper = FormHelper(self)
        self.helper.attrs['autocomplete'] = 'off'
        self.helper.form_tag = False
        self.fields["item_type"].widget.attrs["disabled"] = True
        self.helper.layout = Layout(
            BS5Accordion(
                AccordionGroup(
                    "Customer",
                    Field(
                        'profile', id="id_profile",
                        type="hidden", value=None),
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
                    Field('item', id="id_item", type="hidden"),
                    FloatingField(
                        'item_type',
                        onchange="validateDates()",
                        wrapper_class='col-12 p-0'),
                    FloatingField(
                        'start_date',
                        onchange='validateDates()',
                        wrapper_class='col-12 p-0'),
                    FloatingField(
                        'end_date',
                        onchange='validateDates()',
                        wrapper_class='col-12 p-0'),
                    Div(
                        Div(
                            HTML(""),
                            css_class="card card-body py-1 mb-3",
                            id="stock-collapse-inner"
                        ),
                        css_class="collapse",
                        css_id="stock-collapse"
                    ),
                    FloatingField(
                        'cost_initial',
                        wrapper_class='col-12 p-0'),
                    FloatingField(
                        'cost_week',
                        wrapper_class='col-12 p-0')
                ),
                AccordionGroup(
                    'Payment',
                    Div(
                        FloatingField(
                            'invoice_notes',
                            wrapper_class='col-12 p-0',
                            style="height: 6.5rem;"),
                        css_class="form-floating"
                    ),
                    Submit(
                        'submit-order', 'Complete Payment',
                        css_id='submit-order',
                        css_class="col-12 btn default-button"
                        " d-flex justify-content-center align-items-center"
                    ),
                ),
                flush=True,
                always_open=False,
            ),
        )
