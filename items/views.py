# from datetime import datetime

# from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404  # , redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .models import Item
from .forms import ItemTypeForm, ItemForm


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
    print(request.user.profile.account_type)
    template = 'items/item.html'
    context = {
        # 'current_user': request.user,
        'item_id': item.id,
        'item_serial': item.item_serial,
        'item_image': item.item_type.image,
        'item_type_name': item.item_type.name,
        'image_border': item.item_css_status(),
        'account_type': account_type,
        'item_type_form': ItemTypeForm(account_type=account_type, instance=item.item_type),
        'item_form': ItemForm(account_type=account_type, instance=item)
    }

    return render(request, template, context)
