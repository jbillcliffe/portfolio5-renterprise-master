from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Button, HTML, Reset
# , Row  # , Submit
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
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.attrs['autocomplete'] = 'off'
        self.helper.form_tag = False

        if self.account_type == "Administrator":
            self.fields['item_serial'].widget.attrs['disabled'] = False
        else:
            self.fields['item_serial'].widget.attrs['disabled'] = True

        self.fields['item_type'].widget.attrs['disabled'] = True
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
                # Dropdown button menu for types + categories.
                # Created with help from :
                # https://getbootstrap.com/docs/5.3/forms/input-group/
                Div(
                    HTML(
                        '<img class="item-image img-fluid border-black" '
                        'id="edit-type-image" '
                        'src="{% if not item_type_image %}'
                        '{{STATIC_URL}}"images/default.webp" %}'
                        '{% else %}'
                        '{{ item_type_image.url }}{% endif %}" '
                        'alt="{% if not item_type_image %}'
                        'default no image'
                        '{% else %}'
                        '{{ item_type_name }}{% endif %}">'
                    ),
                    css_class="d-flex col-12 pb-3"
                ),
                Div(
                    StrictButton(
                        'Categories',
                        css_class=(
                            "col-4 btn default-button dropdown-toggle mb-3"),
                        data_bs_toggle="dropdown",
                        aria_expanded="false"
                    ),
                    FloatingField(
                        'category',
                        css_class="rounded-end",
                        wrapper_class="p-0"),
                    HTML(
                        '<ul class="dropdown-menu">'
                        '{% for type in all_types %}'
                        '   {% ifchanged type.category %}'
                        '       <li>'
                        '           <a class="dropdown-item '
                        '{% if type.category == item_type_category %}'
                        'list-active{% else %}{% endif %}" '
                        '{% if type.category == item_type_category %}'
                        '{% else %}'
                        'onclick="'
                        'setTypeCategory(\'{{ type.category }}\')"'
                        '{% endif %} >'
                        '               {{ type.category }}'
                        '           </a>'
                        '       </li>'
                        '       {% endifchanged %}'
                        '   {% endfor %}'
                        '</ul>'
                    ),
                    css_class="row input-group order-1 m-0 p-0"
                ),
                Div(
                    StrictButton(
                        'Types',
                        css_class=(
                            "col-4 btn default-button dropdown-toggle mb-3"),
                        data_bs_toggle="dropdown",
                        aria_expanded="false"
                    ),
                    FloatingField(
                        'name',
                        css_class="rounded-end",
                        wrapper_class="p-0"),
                    HTML(
                        '<ul class="dropdown-menu">'
                        '   {% for type in all_types %}'
                        '   {% if type.category == item_type_category %}'
                        '       <li class="edit-type-list-item" '
                        '        id="type-name-list-item-{{type.id}}"'
                        '        data-name="{{ type }}"'
                        '        data-img="{{ type.image }}">'
                        '           <a class="dropdown-item '
                        '{% if type.name == item_type_name %}'
                        'list-active{% else %}{% endif %}" '
                        '{% if type.name == item_type_name %}'
                        '{% else %}'
                        'onclick="itemTypeChanged('
                        '\'type-name-list-item-{{type.id}}\'){% endif %}">'
                        '               {{ type.name }}'
                        '           </a>'
                        '       </li>'
                        '   {% else %}'
                        '   {% endif %}'
                        '   {% endfor %}'
                        '</ul>'
                    ),
                    css_class="row input-group order-1 m-0 p-0"
                ),
                FloatingField(
                    "sku",
                    wrapper_class="col-12 order-4 p-0"),
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
                    Reset(
                        'cancel-type-edit', 'Cancel',
                        css_id='edit-type-cancel-button',
                        css_class='danger-button',
                        data_bs_dismiss='modal',
                        onclick='resetFormImage()'),
                    css_class="row modal-footer pb-0"
                ),
                css_id="item-type-edit-modal",
                title="Edit Item Type",
            )
        )
