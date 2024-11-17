# from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.core import serializers
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect  # , reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView

import json

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

        # Work with a duplicate of the original instance, just in case
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

        queryset = ItemType.objects.all()
        item_type_list = list(queryset)

        for x in item_type_list:
            print(x.sku)
        # get_item_types = ItemType.objects.all().values()
        # json_item_types = json.dumps(get_item_types)
        # print(json_item_types)
        # print(get_item_types)
        # item_type_data = serializers.serialize('json', get_item_types)
        # print(item_type_data)
        # item_type_list = list(item_type_data)
        # print(item_type_list)
  
        # for x in get_item_types:
        #     print(x)

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
        'item_type_category': item.item_type.category,
        'item_serial': item.item_serial,
        'item_type_sku': item.item_type.sku,
        'item_income': item.income,
        'item_type_image': item.item_type.image,
        'item_type_name': item.item_type.name,
        'status_css': item.item_css_status(),
        'account_type': account_type,
        'all_types': item_type_list,
        'item_type_form': item_type_form,
        'item_form': item_form,
        'item_type_edit_form': item_type_edit_form,
    }

    return render(request, template, context)


@login_required
def item_type_update(request, type_id):
    """
    View to display the properties of an individual item type
    """
    item_type = get_object_or_404(ItemType, pk=type_id)
    account_type = request.user.profile.get_account_type()

    # When form is submitted.
    if request.method == "POST":

        # Work with a duplicate of the original instance, just in case
        item_type_new = item_type
        # Only need to search for the one prefix, because someone without
        # "edit" should not be able to change the details and they are
        # display only
        # name, sku, category, cost_initial, cost_week, meta_tags

        # selected_type = get_object_or_404(
        #     ItemType,
        #     pk=request.POST['edit-type-item_type'])

        # item_new.type = selected_type
        # item_new.item_type = selected_type
        # item_new.item_serial = request.POST['edit-item-item_serial']
        item_type_new.name = request.POST['edit-type-name']
        item_type_new.sku = request.POST['edit-type-sku']
        item_type_new.category = request.POST['edit-type-category']
        item_type_new.cost_initial = request.POST['edit-type-cost_initial']
        item_type_new.cost_week = request.POST['edit-type-cost_week']
        # [NICE] If time will include a meta tags field
        item_type_new.meta_tags = item_type_new.meta_tags

        try:
            item_type_new.full_clean()
        except ValidationError as e:
            messages.error(
                request, (
                    e,
                    'Item type data is not valid.'
                    'Please check the validation prompts.'
                )
            )
            pass

        # item_type_new.save()

        # Display a message to the user to show it has worked
        # messages.success(
        #     request,
        #     'Item successfully updated'
        # )

        # return redirect('item_view', item_id=item_new.id)

    # else:
        # The query is a GET. So data/context/template needs to
        # sent to the form to load.
        # if account_type == "Administrator":
        #     extra_prefix = "edit-"

        # item_form = ItemForm(
        #     account_type=account_type,
        #     instance=item, prefix=f"{extra_prefix}item")
        # item_type_form = ItemTypeForm(
        #     account_type=account_type,
        #     instance=item.item_type, prefix="type")
        # item_type_edit_form = ItemTypeEditForm(
        #     account_type=account_type,
        #     instance=item.item_type, prefix="edit-type")

    # Set template and context
    # template = 'items/item.html'
    # context = {
    #     # 'current_user': request.user,
    #     'item_id': item.id,
    #     'item_serial': item.item_serial,
    #     'item_income': item.income,
    #     'item_image': item.item_type.image,
    #     'item_type_name': item.item_type.name,
    #     'image_border': item.item_css_status(),
    #     'account_type': account_type,
    #     'item_type_form': item_type_form,
    #     'item_form': item_form,
    #     'item_type_edit_form': item_type_edit_form,
    # }

    # return render(request, template, context)