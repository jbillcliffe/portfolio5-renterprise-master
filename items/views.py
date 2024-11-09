# from datetime import datetime

# from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .models import Item
# from .forms import ItemForm, ItemTypeForm


@method_decorator(login_required, name='dispatch')
class ItemList(ListView):
    """
    Class ListView to display the items into a table.
    """
    paginate_by = 10
    model = Item
    template_name = "items/item_list.html"

    def get_context_data(self, **kwargs):
        context = super(ItemList, self).get_context_data(**kwargs)
        return context
