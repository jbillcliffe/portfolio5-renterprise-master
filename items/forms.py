from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Button  # , Row  # , Submit
from crispy_forms.bootstrap import StrictButton, Modal
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
                    css_class='inline-form-button col-1 mb-3',
                    data_bs_toggle='modal',
                    data_bs_target="#item-type-edit-modal",
                ),
                # <button type="button" data-toggle="modal" data-target="#myModal">Launch modal</button>

                # <div id="item_type_edit_modal" class="modal" aria-labelledby="modal_title_id-label" role="dialog" tabindex="-1"> 
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


class ItemTypeEditForm(forms.ModelForm):

    """
    Defining the ItemTypeEditForm, assigning correctly formatted
    labels to the fields and declaring the fields to display
    for creation. Into a modal which is initated from a button on the item view
    """
    # name|sku|category|cost_initial|cost_week|image|meta_tags

    class Meta:
        model = ItemType
        exclude = ["meta_tags"]

        # With fixtures, meta tags were added in, but that is a NICE
        # feature to look to be able to edit or add more.
        labels = {
            "image": "Image",
            "name": "Name",
            "sku": "SKU",
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
        self.helper.form_tag = True
        self.helper.form_action = 'item_type_update'

        # These cannot be edited from the item view by default
        self.fields['name'].required = True
        self.fields['sku'].required = True
        self.fields['category'].required = True
        self.fields['cost_initial'].required = True
        self.fields['cost_week'].required = True

        self.helper.layout = Layout(
            Modal(
                FloatingField(
                    "name",
                    wrapper_class="col-12 order-2 p-0"),
                FloatingField(
                    "sku",
                    wrapper_class="col-12 order-4 p-0"),
                # FloatingField(
                #     "category",
                #     wrapper_class="col-12 order-2 p-0"),
                # Dropdown button menu to use categories, created with help
                # https://getbootstrap.com/docs/5.3/forms/input-group/
                Div(

                    css_class="input-group mb-3"
                ),


                # <div class="input-group mb-3">
                #     <input type="text" class="form-control" aria-label="Text input with dropdown button">
                #     <button class="btn btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">Dropdown</button>
                #     <ul class="dropdown-menu dropdown-menu-end">
                #         <li><a class="dropdown-item" href="#">Action</a></li>
                #         <li><a class="dropdown-item" href="#">Another action</a></li>
                #         <li><a class="dropdown-item" href="#">Something else here</a></li>
                #         <li><hr class="dropdown-divider"></li>
                #         <li><a class="dropdown-item" href="#">Separated link</a></li>
                #     </ul>
                # </div>

                FloatingField(
                    "cost_initial",
                    wrapper_class="col-12 order-4 p-0"),
                FloatingField(
                    "cost_week",
                    wrapper_class="col-12 order-5 p-0"),
                # Crispy forms modal does not automatically use a modal footer
                Div(
                    Button(
                        'submit-type-edit', 'Update Item Type',
                        css_id='edit-type-submit-button',
                        css_class='default-button mb-2',
                        onclick="submitItemTypeForm(event)"),
                    Button(
                        'cancel-type-edit', 'Cancel',
                        css_id='edit-type-cancel-button',
                        css_class='danger-button',
                        data_bs_dismiss='modal',
                        onclick='resetEditTypeForm()'),
                    css_class="row modal-footer pb-0"
                ),
                css_id="item-type-edit-modal",
                title="Edit Item Type",
            )
        )
