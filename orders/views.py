from django.conf import settings
from django.contrib import messages
from django.forms import inlineformset_factory

from django.shortcuts import render, get_object_or_404, redirect

from .forms import OrderForm
from .models import Order
from profiles.models import Profile
from items.models import Item, ItemType


# Create your views here.
def order_create(request):

    account_type = request.user.profile.get_account_type()

    if account_type == 'Customer':
        messages.error(
            request,
            "Permission Denied : A customer cannot create an order")
        return redirect('menu')
    else:
        order_form = OrderForm()
        # order_item = Order()
        inline_item_set = inlineformset_factory(
            Item, Order,  fields=["item"],
            fk_name='item', can_delete=False
        )
        inline_profile_set = inlineformset_factory(
            Profile, Order, fields=["profile"],
            fk_name='profile', can_delete=False
        )

        # if request.method == 'POST':
        #     form = OrderForm(request.POST)
        #     if form.is_valid():
        #         order = form.save()
        #         messages.success(request, 'New order has been created')
        #         # return redirect(reverse('or', args=[product.id]))
        #     else:
        #         messages.error(
        #             request,
        #             'Failed to create the order.'
        #             ' Please ensure the form is valid.'
        #         )
        # else:
        #     form = OrderForm()

        template = 'orders/order_create.html'
        context = {
            'order_form': order_form,
            'inline_item_form': inline_item_set,
            'inline_profile_form': inline_profile_set,
        }

        return render(request, template, context)
