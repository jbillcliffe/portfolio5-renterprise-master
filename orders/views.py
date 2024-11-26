from datetime import datetime
from decimal import Decimal
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.db.models import When
from django.contrib.sessions.models import Session

from .forms import OrderForm
from .models import Order, Invoice
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

    account_type = request.user.profile.get_account_type()

    sessions = Session.objects.iterator()
    for session in sessions:
        data = session.get_decoded()
        data["session_key"] = session.session_key 
        print(data)

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
                'user': request.POST['user'],
                'first_name': request.POST['first_name'],
                'last_name': request.POST['last_name'],
                # Added full name in for stripe
                'full_name': (
                    f"{request.POST['first_name']}"
                    f" {request.POST['last_name']}"
                ),
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
                'created_by': request.user,
                # Accordion - Payment
                'invoice_notes': request.POST['invoice_notes'],
            }

            print(" --- FORM DATA --- ")
            print(form_data)

            if form_data['profile'] is None:

                # Programmatically Creating a user object :
                # -----from models.py of UserManager
                # If password is None then
                # return a concatenation of UNUSABLE_PASSWORD_PREFIX
                # and a random string, which disallows logins.
                # So this can be left blank and can be authorised
                # for logins at another point

                # First check there is no user matching these fields.
                # The combination of first_name, last_name and email
                # should be unique and provide enough to determine
                # if a user exists
                user_new, user_created = User.objects.get_or_create(
                    first_name=form_data['first_name'],
                    last_name=form_data['last_name'],
                    email=form_data['email'],
                    defaults={
                        "is_superuser": False,
                        "is_staff": False,
                    }
                )

                print(" --- USER DATA --- ")
                print(f"Created? - {user_created} : {user_new}")
                # If it found a user it will check there is also no profile
                #
                # If it did not, it will create a new one because there cannot
                # be a profile without a user.

                profile_new, profile_created = Profile.objects.get_or_create(
                    user=user_new,
                    defaults={
                        "address_line_1": form_data['address_line_1'],
                        "address_line_2": form_data['address_line_2'],
                        "address_line_3": form_data['address_line_3'],
                        "town": form_data['town'],
                        "county": form_data['county'],
                        "country": form_data['country'],
                        "postcode": form_data['postcode'],
                        "phone_number": form_data['phone_number'],
                    }
                )
                print(" --- PROFILE DATA --- ")
                print(f"Created? - {profile_created} : {profile_new}")
                # The "profile_new" profile object will be an instance of a
                # pre-existing or new user from these two queries.
                # print("Profile - From None")
                # print(profile_new)
            else:
                # print("Profile - From Form")
                profile_new = Profile.objects.get(pk=form_data['profile'])
                print(" --- EXISTING PEOFILE DATA FROM CUSTOMER PAGE --- ")
                print(profile_new)

            # Create a model object from some of the form data and save()
            new_order = Order.objects.create(
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

            new_order.save()
            print(" --- NEW ORDER DATA --- ")
            print(new_order)

            # Create an invoice with a blank payment reference and status of 0
            # This will then attach a "bill" to an order, which will be :
            # 1. immediately paid
            # 2. left as unpaid (customer cannot pay)
            #
            # If unpaid there needs to be a way to determine if the customer
            # is returning to pay and if they are not.

            # If there were additional notes, add them on what would be
            # a separate line in a string.
            invoice_note_list = ["Initial Rental Payment."]
            if form_data['invoice_notes']:
                invoice_note_list.append[form_data['invoice_notes']]
            invoice_note_final = '\n'.join(invoice_note_list)
            print(" --- FINAL INVOICE NOTES --- ")
            print(invoice_note_final)

            new_invoice = Invoice.objects.create(
                created_on=datetime.today,
                created_by=request.user,
                order=new_order,
                note=invoice_note_final,
                due_on=datetime.today,
                amount_paid=Decimal(form_data['cost_initial']),
                status=0,
                stripe_pid='',
            )
            new_invoice.save()
            print(" --- NEW INVOICE DATA --- ")
            print(new_invoice)
            request.session['new_order'] = form_data
            request.session['new_order_id'] = new_order.id
            request.session['new_invoice'] = new_invoice

            stripe_new_order_payment()

        else:
            # It is a get request from form so return an empty
            # form
            order_form = OrderForm()

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


def stripe_new_order_payment(request):

    # Using a hosted payment page. Greater security provided
    # Check session data required
    print("--- SESSION ORDER ---")
    print(request.session['new_order'])
    print("--- SESSION INVOICE ---")
    print(request.session['new_invoice'])

    stripe_order = request.session["new_order"]
    stripe_order_id = request.session["new_order_id"]
    stripe_line_item = (
        Item.objects.get(pk=stripe_order.item)
    )

    stripe_price = (
        round(stripe_line_item.item_type.cost_initial * 100)
    )
    stripe_ref = (
        f"{stripe_order.last_name}_{stripe_order_id}"
    )

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    stripe_customer = stripe.Customer.create(
        name=stripe_order.full_name,
        email=stripe_order.email,
        address={
            "line1": stripe_order.address_line_1,
            "line2": stripe_order.address_line_2,
            "city": stripe_order.town,
            "state": stripe_order.county,
            "postal_code": stripe_order.postcode,
            "country": "GB"
        },
        shipping={
            "line1": stripe_order.address_line_1,
            "line2": stripe_order.address_line_2,
            "city": stripe_order.town,
            "state": stripe_order.county,
            "postal_code": stripe_order.postcode,
            "country": "GB"
        },
        phone=stripe_order.phone_number
    )

    update_profile_stripe = Profile.objects.get(user=stripe_order.user)
    update_profile_stripe.stripe_id = stripe_customer
    update_profile_stripe.save()
    print("--- Stripe customer --- ")
    print(stripe_customer)
    print("--- Stripe customer pt2. ---")
    print(update_profile_stripe.values())

    # These will be in a modal.
    stripe_success_url = (
        f"https://{request.META['HTTP_HOST']}"
        "/order/create/success?session_id={CHECKOUT_SESSION_ID}")
    stripe_cancel_url = (
        f"https://{request.META['HTTP_HOST']}"
        f"/order/create/cancel")

    print(f"SUCCESS URL : {stripe_success_url}")

    # price_data -> product_date is used to generate at runtime,
    # price would require the object to exist on Stripe
    # and so would price_data -> product

    # Tax Code : https://docs.stripe.com/tax/tax-codes?type=services

    stripe.checkout.Session.create(
        customer=stripe_customer.id,
        customer_email=stripe_order.email,
        client_reference_id=stripe_ref,
        line_items=[{
            "price_data": {
                "currency": f"{settings.STRIPE_CURRENCY}",
                "product_data": {
                    "name": f"{stripe_line_item.item_type.name}",
                    "images": f"{stripe_line_item.item_type.image}",
                    "tax_code": "txcd_20030000"
                },
                "tax_behavior": "exclusive",
                "unit_amount": stripe_price
            },
            "quantity": 1
        }],
        mode="payment",
        success_url=stripe_success_url,
        cancel_url=stripe_cancel_url,
        payment_intent_data={"setup_future_usage": "off_session"}
    )


def order_create_success(request, session_id):
    # Set your secret key. Remember to switch to your live secret key in production.
    # See your keys here: https://dashboard.stripe.com/apikeys

    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_session = stripe.checkout.Session.retrieve(request.args.get('session_id'))
    stripe_customer = stripe.Customer.retrieve(stripe_session.stripe_customer)

    template = 'orders/order_create_success.html'
    context = {
        'stripe_session': stripe_session,
        'stripe_customer': stripe_customer,
        'end_of_order': True,
    }

    return render(request, template, context)
