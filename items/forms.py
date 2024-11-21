from django import forms
from django.shortcuts import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Reset, Submit
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

        for field in self.fields:
            self.fields[field].required = True
            if field == 'item_serial':
                if self.account_type == "Administrator":
                    self.fields[field].widget.attrs['disabled'] = False
                else:
                    self.fields[field].widget.attrs['disabled'] = True

        self.helper.layout = Layout(
            Div(
                FloatingField(
                    "item_type",
                    wrapper_class=(
                        "flex-md-row col-12 col-sm-10 p-0"),
                    ),
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
        # self.fields['category'].widget.attrs['disabled'] = True
        # self.fields['cost_initial'].widget.attrs['disabled'] = True
        # self.fields['cost_week'].widget.attrs['disabled'] = True

        # self.fields['category'].required = True
        # self.fields['cost_initial'].required = True
        # self.fields['cost_week'].required = True

        for field in self.fields:
            self.fields[field].required = True
            self.fields[field].widget.attrs['disabled'] = True

        self.helper.layout = Layout(
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

    # image = forms.ImageField(
    #     label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        """
        """
        self.item_id = kwargs.pop('item_id', None)
        self.account_type = kwargs.pop('account_type', None)
        super().__init__(*args, **kwargs)
        self.type_id = self.instance.id
        self.helper = FormHelper(self)
        self.helper.attrs['autocomplete'] = 'off'
        self.helper.form_tag = True
        # self.helper.form_action = 'item_type_update'
        self.helper.form_action = reverse(
            'item_type_update_inline',
            kwargs={
                "item_id": self.item_id,
                "type_id": self.type_id
            }
        )

        # These cannot be edited from the item view by default
        # self.fields['name'].required = True
        # self.fields['sku'].required = True
        # self.fields['category'].required = True
        # self.fields['cost_initial'].required = True
        # self.fields['cost_week'].required = True

        for field in self.fields:
            self.fields[field].required = True
            self.fields[field].widget.attrs['disabled'] = False

        # self.fields['image'].widget.attrs['disabled'] = True

        self.helper.layout = Layout(
            Modal(
                # Dropdown button menu for types + categories.
                # Created with help from :
                # https://getbootstrap.com/docs/5.3/forms/input-group/
                HTML(
                    '<strong id="id-edit-progress"'
                    'class="text-primary mt-0 mb-1 d-none">'
                    'Currently Editing</strong>'
                ),
                HTML(
                    '<img class="item-image img-fluid border-black'
                    ' d-flex justify-content-center mb-3 p-0" '
                    'id="edit-type-image" '
                    'src="{% if not item_type_image %}'
                    '{{ STATIC_URL }}"images/default.webp" %}'
                    '{% else %}'
                    '{{ item_type_image.url }}{% endif %}" '
                    'alt="{% if not item_type_image %}'
                    'default no image'
                    '{% else %}'
                    '{{ item_type_name }}{% endif %}">'
                ),
                HTML(
                    '{% include "items/includes/custom_file_input.html"'
                    ' with image_sent_url=item_type_image.url %}'
                ),
                Div(
                    StrictButton(
                        'Categories',
                        css_class=(
                            "col-4 btn default-button"
                            " dropdown-toggle mb-3 d-flex "
                            " justify-content-center align-items-center"
                            " mb-3 p-0"),
                        data_bs_toggle="dropdown",
                        aria_expanded="false"
                    ),
                    FloatingField(
                        'category',
                        css_class="rounded-end",
                        onchange="typeCategoryChanged(this.value, \'input\')",
                        wrapper_class="p-0"),
                    HTML(
                        '<ul class="dropdown-menu">'
                        '{% for type in all_types %}'
                        '   {% ifchanged type.category %}'
                        '       <li>'
                        '<a class="dropdown-item type-category-list-item'
                        '{% if type.category == item_type_category %}'
                        ' list-active{% else %}{% endif %}" '
                        'onclick="'
                        'typeCategoryChanged(\'{{ type.category }}\', \'drop\')">'
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
                        css_id="id-types-dropdown-btn",
                        css_class=(
                            "col-4 btn default-button"
                            " dropdown-toggle mb-3 d-flex "
                            " justify-content-center align-items-center"
                            " mb-3 p-0"),
                        data_bs_toggle="dropdown",
                        aria_expanded="false"
                    ),
                    FloatingField(
                        'name',
                        css_class="rounded-end",
                        onchange="typeChanged()",
                        wrapper_class="p-0"),
                    HTML(
                        '<ul class="dropdown-menu">'
                        '   {% for type in all_types %}'
                        '       <li id="li-{{ type.id }}" '
                        'class="edit-type-list-item '
                        '{% if type.category == item_type_category %}'
                        '{% else %}d-none{% endif %}">'
                        '           <a id="li-a-{{ type.id }}" '
                        'class="dropdown-item '
                        'type-name-list-item '
                        '{% if type.name == item_type_name %}'
                        'list-active{% else %}{% endif %}" '
                        'onclick="typeChanged(\'{{ type.id }}\')"'
                        ' data-img=\'{{ type.image }}\''
                        ' data-category=\'{{ type.category }}\''
                        ' data-sku=\'{{ type.sku }}\''
                        ' data-initial=\'{{ type.cost_initial }}\''
                        ' data-week=\'{{ type.cost_week }}\''
                        '>'
                        '               {{ type.name }}'
                        '           </a>'
                        '       </li>'
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
                    onfocusout="setTwoDecimalPlaces(this.id, this.value)",
                    wrapper_class="col-12 order-4 p-0"),
                FloatingField(
                    "cost_week",
                    onfocusout="setTwoDecimalPlaces(this.id, this.value)",
                    wrapper_class="col-12 order-5 p-0"),
                # Crispy forms modal does not automatically use a modal footer
                Div(
                    # Button(
                    #     'submit-type-edit', 'Update Item Type',
                    #     css_id='edit-type-submit-button',
                    #     css_class='default-button mb-2',
                    #     onclick="submitItemTypeForm(event)"),
                    Submit(
                        'submit-type-edit', 'Update Item Type',
                        css_id='edit-type-submit-button',
                        css_class='default-button mb-2'
                    ),
                    Reset(
                        'cancel-type-edit', 'Cancel',
                        css_id='edit-type-cancel-button',
                        css_class='danger-button',
                        data_bs_dismiss='modal',
                        onclick='resetForm()'),
                    css_class="row modal-footer pb-0"
                ),
                css_id="item-type-edit-modal",
                title="Edit Item Type",
            )
        )
