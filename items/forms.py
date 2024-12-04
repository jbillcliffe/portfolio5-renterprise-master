from django import forms
from django.shortcuts import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Reset, Submit, Field
from crispy_forms.bootstrap import StrictButton, Modal
from crispy_bootstrap5.bootstrap5 import FloatingField

from .models import Item, ItemType


class ItemForm(forms.ModelForm):
    """
    Defining the ItemForm, assigning correctly formatted
    labels to the fields and declaring the fields to display
    for creation. ItemTypeForm is also joined to this for viewing.
    """
    class Meta:
        # Assigning the model to the form, fields to be active
        # and the labels associated to the fields.
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
            elif field == 'item_type':
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
    


class ItemCreateForm(forms.ModelForm):
    """
    Defining the ItemForm, assigning correctly formatted
    labels to the fields and declaring the fields to display
    for creation. ItemTypeForm is also joined to this for viewing.
    """
    class Meta:
        # Assigning the model to the form, fields to be active
        # and the labels associated to the fields.
        model = Item
        fields = ['item_type', 'item_serial']
        labels = {
            "item_type": "Item Type",
            "item_serial": "Serial No.",
        }

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """

        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.attrs['autocomplete'] = 'off'
        self.helper.form_tag = False
        # Starts as true, to force a category selection first.
        self.fields['item_type'].widget.attrs['disabled'] = True

        self.helper.layout = Layout(
            # Create the left side div of the form (class=row) which
            # will hold the image. It will then stack on top when the
            # screen width shrinks
            Div(
                # Create an image display, with default blank image.
                # An image can then be shown when a type is chosen
                HTML(
                    '<img class="item-image img-fluid border-black'
                    ' d-flex justify-content-center p-0" '
                    'id="id-image-display"'
                    'src="/static/images/default.webp"'
                    'alt="default no image">'
                ),
                css_class=(
                    'd-flex flex-column '
                    'd-lg-block col-12 col-lg-3 col-xxl-4 pb-3')
            ),
            # Create the right side div, which will have the
            # category select, the type select and serial input.
            Div(
                # Create the category floating field
                Div(
                    HTML(
                        '<select name="category-select"'
                        ' class="select form-select"'
                        ' placeholder="Category"'
                        ' id="id-category-select"'
                        ' onchange="getAvailableTypes()">'
                        '<option selected>---------</option>'
                        '{% for type in all_types %}'
                        '   {% ifchanged type.category %}'
                        '<option>{{ type.category }}</option>'
                        '   {% endifchanged %}'
                        '{% endfor %}'
                        '</select>'
                        '<label for="id-category-select">'
                        'Item Category</label>'
                    ),
                    css_id="div_id_category",
                    css_class="form-floating order-1 mb-3"
                ),
                Div(
                    HTML(
                        '<select name="item_type"'
                        ' class="select form-select"'
                        ' placeholder="item_type"'
                        ' id="id_item_type"'
                        ' onchange="displayTypeImage()"'
                        ' required'
                        ' disabled>'
                        '<option>---------</option>'
                        '{% for type in all_types %}'
                        '<option '
                        ' class="type-option-item"'
                        ' data-category="{{ type.category }}"'
                        ' data-image="{{ type.image.url }}"'
                        ' value="{{ type.id }}">'
                        '{{ type.name }}'
                        '</option>'
                        '{% endfor %}'
                        '</select>'
                        '<label for="id_item_type">'
                        'Item Type'
                        '<span class="asteriskField">*</span>'
                        '</label>'
                    ),
                    css_id="div_id_item_type",
                    css_class="form-floating mb-3 col-12 order-2 p-0"
                ),

                # Create item_type as HTML to include data-category
                # FloatingField(
                #     "item_type",
                #     wrapper_class="col-12 order-2 p-0"),
                # Create item_serial field from model
                FloatingField(
                    "item_serial",
                    wrapper_class="col-12 order-3 p-0"),

                # Set class for the right side div
                css_class="col-12 col-lg-9 col-xxl-8"
            )
        )


class ItemStatusForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['status']
        labels = {
            "status": "Status",
        }

    def __init__(self, *args, **kwargs):

        self.item_id = kwargs.pop('item_id')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.attrs['autocomplete'] = 'off'
        self.helper.form_tag = True
        self.helper.form_action = reverse(
            'item_status_edit',
            kwargs={
                'item_id': self.item_id,
            }
        )
        self.helper.layout = Layout(
            Modal(
                HTML(
                    '{% with status_array=template_status %}'
                    '{% for x, y in status_array %}'
                    # Create a div at each one.
                    '<div class="form-check form-switch mb-3">'
                    '<input'
                    ' class="form-check-input {{ x }} me-3"'
                    ' type="checkbox" role="switch"'
                    ' onchange="statusSwitchChanger(\'{{ x }}\')"'
                    ' value={{ forloop.counter0 }}'
                    ' id="id-status-{{ x }}">'
                    '<label class="form-check-label"'
                    ' for="id-status-{{ x }}">'
                    '{{ y }}</label>'
                    '</div>'
                    '{% endfor %}'
                    '{% endwith %}'
                ),
                Field('status', type="hidden", id="id_status"),
                HTML(
                    '<input name="status-item_id"'
                    ' id="id_status_id" value="{{ item_id }}" hidden>'),
                # Submit("status-submit", "Submit"),
                Div(
                    # Submit means this defaults to performing the
                    # "form action"
                    Submit(
                        'submit-status-edit', 'Update Status',
                        css_id='edit-status-submit-button',
                        css_class='default-button mb-2'
                    ),
                    # Returns the form to it's original state.
                    # Removing "editing" status field, making sure the type
                    # dropdown isn't disabled, resetting the image display
                    # and image text area are done in JS
                    Reset(
                        'cancel-status-edit', 'Cancel',
                        css_id='edit-status-cancel-button',
                        css_class='danger-button',
                        data_bs_dismiss='modal'),
                    css_class="row modal-footer justify-content-center pb-0"
                ),
                css_id="item-status-change-modal",
                css_class="modal-sm",
                data_bs_backdrop="static",
                data_bs_keyboard="false",
                title="Set Item Status"
            )
        )


class ItemTypeForm(forms.ModelForm):
    """
    Defining the ItemTypeForm, assigning correctly formatted
    labels to the fields and declaring the fields to display
    for creation. This is a viewing form as part of the ItemForm.
    Edits for types are done inline, or could be accessible from
    another page.
    """

    class Meta:
        # Assigning the model to the form, fields to be active
        # and the labels associated to the fields.
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

    class Meta:
        # Assigning the model to the form, fields to be active
        # and the labels associated to the fields. In this case,
        # all fields are included except for meta_tags [NICE]
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
        self.item_id = kwargs.pop('item_id', None)
        self.account_type = kwargs.pop('account_type', None)
        super().__init__(*args, **kwargs)
        self.type_id = self.instance.id
        self.helper = FormHelper(self)
        self.helper.attrs['autocomplete'] = 'off'
        self.helper.form_tag = True
        self.helper.form_id = "item-inline-type-form-id"
        self.helper.form_action = reverse(
            'item_type_update_inline',
            kwargs={
                "item_id": self.item_id,
                "type_id": self.type_id
            }
        )

        for field in self.fields:
            self.fields[field].required = True
            self.fields[field].widget.attrs['disabled'] = False

        # Except sku, make that readonly as this shouldn't be changed.
        # They are unique, so it should be fixed
        self.fields['sku'].widget.attrs['readonly'] = True

        self.helper.layout = Layout(
            Modal(
                # Dropdown button menu for types + categories.
                # Created with help from :
                # https://getbootstrap.com/docs/5.3/forms/input-group/

                # A simple display and also a way of checking edit progress.
                # This stops unnecessary form reloads.
                HTML(
                    '<strong id="id-edit-progress"'
                    'class="text-primary mt-0 mb-1 d-none">'
                    'Currently Editing</strong>'
                ),
                # Setting the image display for the type
                HTML(
                    '<img class="item-image img-fluid border-black'
                    ' d-flex justify-content-center mb-3 p-0" '
                    'id="edit-type-image" '
                    'src="{% if not item_type_image %}'
                    '{{ STATIC_URL }}"images/default.webp"'
                    '{% else %}'
                    '{{ item_type_image.url }}'
                    '{% endif %}" '
                    'alt="{% if not item_type_image %}'
                    'default no image'
                    '{% else %}'
                    '{{ item_type_name }}{% endif %}">'
                ),
                # Include this file, its a long block which has a custom
                # customisation of the ClearableFileInput.
                HTML(
                    '{% include "items/includes/custom_file_input.html"'
                    ' with image_sent_url=item_type_image.url %}'
                ),
                # A row which has Category dropdown and category input field
                Div(
                    # Creating the category dropdown button.
                    # StrictButton ensures it is a <button> (not <a>)
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
                    # Category text input+ associated function for
                    # change in text
                    FloatingField(
                        'category',
                        css_class="rounded-end",
                        onchange="typeCategoryChanged(this.value, \'input\')",
                        wrapper_class="p-0"),
                    # Creating the dropdown list of categories for selection
                    HTML(
                        '<ul class="dropdown-menu">'
                        '{% for type in all_types %}'
                        '   {% ifchanged type.category %}'
                        '       <li>'
                        '<a class="dropdown-item type-category-list-item'
                        '{% if type.category == item_type_category %}'
                        ' list-active{% else %}{% endif %}" '
                        'onclick="'
                        'typeCategoryChanged('
                        '\'{{ type.category }}\', \'drop\')">'
                        '               {{ type.category }}'
                        '           </a>'
                        '       </li>'
                        '       {% endifchanged %}'
                        '   {% endfor %}'
                        '</ul>'
                    ),
                    css_class="row input-group order-1 m-0 p-0"
                ),
                # A row which has type(name) dropdown
                # and type(name) input field
                Div(
                    # Creating the type(name) dropdown button.
                    # StrictButton ensures it is a <button> (not <a>)
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
                    # Type(name) text input + associated function for
                    # change in text
                    FloatingField(
                        'name',
                        css_class="rounded-end",
                        onchange="typeChanged()",
                        wrapper_class="p-0"),
                    # Creating the dropdown list of types(names)
                    # for selection
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
                # SKU input field
                FloatingField(
                    "sku",
                    wrapper_class="col-12 order-4 p-0"),
                # Initial Cost input field
                FloatingField(
                    "cost_initial",
                    onfocusout="setTwoDecimalPlaces(this.id, this.value)",
                    wrapper_class="col-12 order-4 p-0"),
                # Weekly Cost input field
                FloatingField(
                    "cost_week",
                    onfocusout="setTwoDecimalPlaces(this.id, this.value)",
                    wrapper_class="col-12 order-5 p-0"),
                # Crispy forms modal does not automatically use a modal footer
                # A div which holds the two form buttons, submit and reset
                Div(
                    # Submit means this defaults to performing the
                    # "form action"
                    Submit(
                        'submit-type-edit', 'Update Item Type',
                        css_id='edit-type-submit-button',
                        css_class='default-button mb-2'
                    ),
                    # Returns the form to it's original state.
                    # Removing "editing" status field, making sure the type
                    # dropdown isn't disabled, resetting the image display
                    # and image text area are done in JS
                    Reset(
                        'cancel-type-edit', 'Cancel',
                        css_id='edit-type-cancel-button',
                        css_class='danger-button',
                        data_bs_dismiss='modal',
                        onclick='resetForm()'),
                    css_class="row modal-footer justify-content-center pb-0"
                ),
                css_id="item-type-edit-modal",
                title="Edit Item Type",
                # Send Item Id as the ID for this modal. This stays fixed
                # when creating the dynamic form action
                data_form_id=self.item_id,
                data_bs_backdrop="static",
                data_bs_keyboard="false"
            )
        )
