from datetime import datetime
from decimal import Decimal
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import  User, UserManager
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.db.models import When

from .forms import OrderForm
from .models import Order
from profiles.models import Profile
from items.models import Item, ItemType

import stripe


# @require_POST
# def cache_order_data(request):
#     try:
#         pid = request.POST.get('client_secret').split('_secret')[0]
#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         stripe.PaymentIntent.modify(pid, metadata={
#             #'bag': json.dumps(request.session.get('bag', {})),

#             'save_info': request.POST.get('save_info'),
#             'username': request.user,
#         }) 
#         return HttpResponse(status=200)
#     except Exception as e:
#         messages.error(request, 'Sorry, your payment was not processed')
#         return HttpResponse(content=e, status=400)

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
            order_form = OrderForm(request.POST)
            form_data = {
                # Accordion - Customer
                # user_name will default null, unless order is created
                # from a historical customer. If an order and customer are
                # created at the same time it will need to create the User
                # and profile.
                'user_name': request.POST['user_name'],
                'first_name': request.POST['first_name'],
                'last_name': request.POST['last_name'],
                'email': request.POST['email'],
                'phone_number': request.POST['phone_number'],
                # Accordion - Address
                'address_line_1': request.POST['address_line_1'],
                'address_line_2': request.POST['address_line_2'],
                'address_line_3': request.POST['address_line_3'],
                'town': request.POST['town'],
                'county': request.POST['county'],
                'country': request.POST['country'],
                'postcode': request.POST['postcode'],
                # Accordion - Order
                'item': request.POST['item'],
                'cost_initial': request.POST['cost_initial'],
                'cost_week': request.POST['cost_week'],
                'start_date': request.POST['start_date'],
                'end_date': request.POST['end_date'],
                'created_on': datetime.now,
                'create_by': request.user
            }

            # Creating a user object :
            # -----from models.py of UserManager
            # If password is None then
            # return a concatenation of UNUSABLE_PASSWORD_PREFIX
            # and a random string, which disallows logins.
            # So this can be left blank and can be authorised
            # for logins at another point

            if form_data['user_name'] is None:

                user_new = User.objects.create_user(
                    first_name=form_data['first_name'],
                    last_name=form_data['last_name'],
                    is_superuser=False,
                    email=form_data['email'],
                    is_staff=False,
                    username=check_username(
                        (f"{form_data['first_name']}{form_data['last_name'][0]}"))
            )
            user_new.save()

            profile_new = Profile.objects.create(
                user=user_new,
                address_line_1=form_data['address_line_1'],
                address_line_2=form_data['address_line_2'],
                address_line_3=form_data['address_line_3'],
                town=form_data['town'],
                county=form_data['county'],
                country=form_data['country'],
                postcode=form_data['postcode'],
                phone_number=form_data['phone_number']
            )
            profile_new.save()

            order = Order.objects.create(
                profile=profile_new,
                item=form_data['item'],
                cost_initial=Decimal(form_data['cost_initial']),
                cost_week=Decimal(form_data['cost_week']),
                start_date=datetime.strptime(
                    form_data['start_date'], '%Y-%m-%d'),
                end_date=datetime.strptime(
                    form_data['end_date'], '%Y-%m-%d'),
                created_by=request.user,
                created_on=datetime.now
            )
            order.save()

            # At this point without the invoice, this order is incompete.
            # So assign an invoice that is unpaid, but associate Stripe to it.
        else:
            # Not a post request
            order_form = OrderForm()


            # profile, user = 
    #              item = models.ForeignKey(
    #     Item, on_delete=models.PROTECT, related_name="order_item"
    # )
    # cost_initial = models.DecimalField(max_digits=6, decimal_places=2)
    # cost_week = models.DecimalField(max_digits=6, decimal_places=2)

    # start_date = models.DateField()
    # end_date = models.DateField(blank=True, null=True)
    # created_on = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey(
    #     User, on_delete=models.PROTECT, related_name="order_created_by"
    # )
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
            
        # inline_item_set = inlineformset_factory(
        #     Item, Order,  fields=["item"],
        #     fk_name='item', can_delete=False
        # )
        # inline_profile_set = inlineformset_factory(
        #     Profile, Order, fields=["profile"],
        #     fk_name='profile', can_delete=False
        # )
        

        #     stripe_total = round(100 * 100)
        #     stripe.api_key = stripe_secret_key
        #     intent = stripe.PaymentIntent.create(
        #         amount=stripe_total,
        #         currency=settings.STRIPE_CURRENCY,
        #     )

        # if not stripe_public_key:
        #     messages.warning(request, 'Stripe public key is missing.')

        template = 'orders/order_create.html'
        context = {
            'order_form': order_form,
            # 'stripe_public_key': stripe_public_key,
            # 'client_secret': intent.client_secret,
            'json_item_list': json_item_list,
            'json_order_list': json_order_list,
            'json_item_type_list': json_item_type_list,
        }

        return render(request, template, context)

def check_username(user_name):
    # set initial username to try
    internal_username = user_name

    # set initial value for extra identifier, so first attempt will be
    # "username" then "username1", "username2" and so on ...
    user_number = 1

    while True:
        if User.objects.filter(username=internal_username).exists():
            internal_username = f"{user_name}{user_number}"
            user_number += 1
        else:
            # if false, it means this username doesn't exist,
            # so it can be used
            return internal_username
            break
