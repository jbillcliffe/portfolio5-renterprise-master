from django.conf import settings
from django.contrib import messages
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse

from .forms import OrderForm
from .models import Order
from profiles.models import Profile
from items.models import Item, ItemType

import stripe


@require_POST
def cache_order_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            #'bag': json.dumps(request.session.get('bag', {})),

            'save_info': request.POST.get('save_info'),
            'username': request.us,
        }) 
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment was not processed')
        return HttpResponse(content=e, status=400)


# Create your views here.
def order_create(request):

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    account_type = request.user.profile.get_account_type()

    json_item_list = serialize(
        'json', Item.objects.all(),
        fields=[
            "item_type", "delivery_date", "collect_date",
            "repair_date", "income", "status"],
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

        if request.method == 'POST':
            #order_form = OrderForm(request.POST)
            form_data = {
                'first_name': request.POST['first_name'],
                'last_name': request.POST['last_name'],
                'email': request.POST['email'],
                'phone_number': request.POST['phone_number'],
                
                'address_line_1': request.POST['address_line_1'],
                'address_line_2': request.POST['address_line_2'],
                'address_line_3': request.POST['address_line_3'],
                'town': request.POST['town'],
                'county': request.POST['county'],
                'country': request.POST['country'],
                'postcode': request.POST['postcode'],
                'item_type': request.POST['item_type']
            }
            # id_first_name
            # id_last_name
            # id_email
            # id_phone_number

            # id_address_line_1
            # id_address_line_2
            # id_address_line_3
            # id_town
            # id_county
            # id_country
            # id_postcode

            # id_item_type
            # id_delivery_date
            # id_collect_date
            # id_cost_initial
            # id_cost_week

            # id_invoice_notes
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
        

            stripe_total = round(100 * 100)
            stripe.api_key = stripe_secret_key
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
            )

        if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing.')

        template = 'orders/order_create.html'
        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
            'json_item_list': json_item_list,
            'json_order_list': json_order_list,
            'json_item_type_list': json_item_type_list,
        }

        return render(request, template, context)
