# from datetime import datetime

# from django.contrib import messages
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
# from django.core import serializers
from django.shortcuts import render, get_object_or_404, redirect  # , reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .models import Item, ItemType
from .forms import ItemTypeForm, ItemTypeEditForm, ItemForm


@method_decorator(login_required, name='dispatch')
class ItemList(ListView):
    """
    Class ListView to display the items into a table.
    """
    paginate_by = 10
    model = Item
    template_name = 'items/item_list.html'

    def get_context_data(self, **kwargs):
        context = super(ItemList, self).get_context_data(**kwargs)
        return context


@login_required
def item_view(request, item_id):
    """
    View to display the properties of an individual item
    """

    item = get_object_or_404(Item, pk=item_id)
    account_type = request.user.profile.get_account_type()

    # When form is submitted, note to ignore the ItemType form, they are
    # disabled in the form and they are display only, carrying the values
    # from it's own model for display.
    if request.method == "POST":

        item_new = item
        # Only need to search for the one prefix, because someone without
        # "edit" should not be able to change the details and they are
        # display only
        selected_type = get_object_or_404(
            ItemType,
            pk=request.POST['edit-item-item_type'])
        item_new.type = selected_type
        item_new.item_type = selected_type
        item_new.item_serial = request.POST['edit-item-item_serial']

        try:
            item_new.full_clean()
        except ValidationError as e:
            messages.error(
                request, (
                    e,
                    'Item data is not valid.'
                    'Please check the validation prompts.'
                )
            )
            pass

        item_new.save()

        # Display a message to the user to show it has worked
        messages.success(
            request,
            'Item successfully updated'
        )

        return redirect('item_view', item_id=item_new.id)

    else:
        # The query is a GET. So data/context/template needs to
        # sent to the form to load.
        if account_type == "Administrator":
            extra_prefix = "edit-"

        item_form = ItemForm(
            account_type=account_type,
            instance=item, prefix=f"{extra_prefix}item")
        item_type_form = ItemTypeForm(
            account_type=account_type,
            instance=item.item_type, prefix="type")
        item_type_edit_form = ItemTypeEditForm(
            account_type=account_type,
            instance=item.item_type, prefix="edit-type")

    # Set template and context
    template = 'items/item.html'
    context = {
        # 'current_user': request.user,
        'item_id': item.id,
        'item_serial': item.item_serial,
        'item_income': item.income,
        'item_image': item.item_type.image,
        'item_type_name': item.item_type.name,
        'image_border': item.item_css_status(),
        'account_type': account_type,
        'item_type_form': item_type_form,
        'item_form': item_form,
        'item_type_edit_form': item_type_edit_form,
    }

    return render(request, template, context)
