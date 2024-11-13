from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Hidden
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
            "item_serial": "Serial No."
        }

    def __init__(self, *args, **kwargs):
        self.account_type = kwargs.pop('account_type', None)
        # self.item_type_key = kwargs.pop('item_type_key', None)
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
            # Hidden("item_type_key", self.item_type_key),
            FloatingField("item_type", data_),
            FloatingField("item_serial"),
        )


class ItemTypeForm(forms.ModelForm):
    """
    Defining the ItemTypeForm, assigning correctly formatted
    labels to the fields and declaring the fields to display
    for creation.
    """
    previous_category_tags = ItemType.objects.all()

    class Meta:
        model = ItemType
        fields = ['category', 'cost_initial', 'cost_week']
        # With fixtures, meta tags were added in, but that is a NICE
        # feature.
        labels = {
            # "name": "Type",
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

        if self.account_type == "Administrator":
            # self.fields['name'].widget.attrs['disabled'] = False
            self.fields['category'].widget.attrs['disabled'] = False
            self.fields['cost_initial'].widget.attrs['disabled'] = False
            self.fields['cost_week'].widget.attrs['disabled'] = False
        else:
            # self.fields['name'].widget.attrs['disabled'] = True
            self.fields['category'].widget.attrs['disabled'] = True
            self.fields['cost_initial'].widget.attrs['disabled'] = True
            self.fields['cost_week'].widget.attrs['disabled'] = True

        # self.fields['name'].required = True
        self.fields['category'].required = True
        self.fields['cost_initial'].required = True
        self.fields['cost_week'].required = True

        self.helper.layout = Layout(
            # FloatingField("name"),
            FloatingField("category"),
            FloatingField("cost_initial"),
            FloatingField("cost_week"),
        )
