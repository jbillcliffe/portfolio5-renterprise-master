from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Div
from crispy_forms.bootstrap import StrictButton
from crispy_bootstrap5.bootstrap5 import FloatingField

from .models import Item, ItemType


class ItemForm(forms.ModelForm):
    """
    Defining the ItemForm, assigning correctly formatted
    labels to the fields and declaring the fields to display
    for creation.
    """

    class Meta:
        """
        """
        model = Item
        fields = ['item_type', 'item_serial']
        labels = {
            "item_type": "Type",
            "item_serial": "Serial No.",
        }

    def __init__(self, *args, **kwargs):

        self.account_type = kwargs.pop('account_type', None)
        self.all_types = kwargs.pop('all_types', None)

        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.attrs['autocomplete'] = 'off'
        self.helper.form_tag = False

        if self.account_type == "Administrator":
            self.fields['item_type'].widget.attrs['disabled'] = False
            self.fields['item_serial'].widget.attrs['disabled'] = False
        else:
            self.fields['item_type'].widget.attrs['disabled'] = True
            self.fields['item_serial'].widget.attrs['disabled'] = True

        self.fields['item_type'].required = True
        self.fields['item_serial'].required = True

        self.helper.layout = Layout(
            Div(
                FloatingField(
                    "item_type",
                    wrapper_class=(
                        "flex-md-row col-12 col-sm-10 p-0")),
                StrictButton(
                    '<span class="d-flex flex-row align-items-center gap-3">'
                    '<p class="d-block d-sm-none my-0 white-text">'
                    'Edit Item Type'
                    '</p>'
                    '<i class="bi bi-pen white-text"></i>'
                    '</span>',
                    css_class='inline-form-button col-1 mb-3'
                ),
                css_class="row order-1 p-0 mx-auto"
            ),

            FloatingField(
                "item_serial",
                wrapper_class="col-12 order-3 p-0"),
        )


class ItemTypeForm(forms.ModelForm):
    """
    Defining the ItemTypeForm, assigning correctly formatted
    labels to the fields and declaring the fields to display
    for creation.
    """
    # previous_category_tags = ItemType.objects.all()

    class Meta:
        model = ItemType
        fields = ['category', 'cost_initial', 'cost_week']
        # With fixtures, meta tags were added in, but that is a NICE
        # feature to look to be able to edit or add more.
        labels = {
            "category": "Category",
            "cost_initial": "Initial (£)",
            "cost_week": "Weekly (£)",
        }

    def __init__(self, *args, **kwargs):
        """
        """
        self.account_type = kwargs.pop('account_type', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.attrs['autocomplete'] = 'off'
        self.helper.form_tag = False

        # These cannot be edited from the item view by default
        self.fields['category'].widget.attrs['disabled'] = True
        self.fields['cost_initial'].widget.attrs['disabled'] = True
        self.fields['cost_week'].widget.attrs['disabled'] = True

        self.fields['category'].required = True
        self.fields['cost_initial'].required = True
        self.fields['cost_week'].required = True

        self.helper.layout = Layout(
            # FloatingField("name"),
            FloatingField(
                "category",
                wrapper_class="col-12 order-2 p-0"),
            FloatingField(
                "cost_initial",
                wrapper_class="col-12 order-4 p-0"),
            FloatingField(
                "cost_week",
                wrapper_class="col-12 order-5 p-0"),
        )
