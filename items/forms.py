from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
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
        """
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.attrs['autocomplete'] = 'off'
        self.helper.form_tag = False
        self.fields['item_type'].required = True
        self.fields['item_serial'].required = True

        self.helper.layout = Layout(
            FloatingField("item_type"),
            FloatingField("item_serial"),
        )


class ItemTypeForm(forms.ModelForm):
    """
    Defining the ItemTypeForm, assigning correctly formatted
    labels to the fields and declaring the fields to display
    for creation.
    """
    class Meta:
        model = ItemType
        fields = "__all__"
        labels = {
            "name": "Type",
            "cost_initial": "Initial (£)",
            "cost_week": "Weekly (£)",
        }

    def __init__(self, *args, **kwargs):
        """
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.attrs['autocomplete'] = 'off'
        self.helper.form_tag = False
        self.fields['name'].required = True
        self.fields['cost_initial'].required = True
        self.fields['cost_week'].required = True
        self.helper.layout = Layout(
            FloatingField("name"),
            FloatingField("category"),
            FloatingField("cost_initial"),
            FloatingField("cost_week"),
        )
    # image_url = models.URLField(max_length=1024, null=True, blank=True)
    # image = models.ImageField(null=True, blank=True)
