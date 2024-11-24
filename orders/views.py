from django.conf import settings
from django.contrib import messages
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import inlineformset_factory

from django.shortcuts import render, get_object_or_404, redirect

from .forms import OrderForm
from .models import Order
from profiles.models import Profile
from items.models import Item, ItemType


# Create your views here.
def order_create(request):

    account_type = request.user.profile.get_account_type()

    json_item_list = serialize(
        'json', Item.objects.all(),
        fields=[
            "item_type", "delivery_date", "collect_date",
            "repair_date", "status"],
        cls=DjangoJSONEncoder)

    json_item_type_list = serialize(
        'json', ItemType.objects.all(),
        fields=[
            "cost_initial", "cost_week",
            "image"],
        cls=DjangoJSONEncoder)

    json_order_list = serialize(
        'json', Order.objects.all(), fields=[
            'item', 'start_date', 'end_date'],
        cls=DjangoJSONEncoder)

    if account_type == 'Customer':
        messages.error(
            request,
            "Permission Denied : A customer cannot create an order")
        return redirect('menu')
    else:
        order_form = OrderForm()
        # inline_item_set = inlineformset_factory(
        #     Item, Order,  fields=["item"],
        #     fk_name='item', can_delete=False
        # )
        # inline_profile_set = inlineformset_factory(
        #     Profile, Order, fields=["profile"],
        #     fk_name='profile', can_delete=False
        # )

        template = 'orders/order_create.html'
        context = {
            'order_form': order_form,
            # 'inline_item_form': inline_item_set,
            # 'inline_profile_form': inline_profile_set,
            'json_item_list': json_item_list,
            'json_order_list': json_order_list,
            'json_item_type_list': json_item_type_list,
        }

        return render(request, template, context)
