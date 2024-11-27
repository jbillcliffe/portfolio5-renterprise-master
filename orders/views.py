from datetime import datetime
from datetime import timedelta
from decimal import Decimal
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect  # get_object_or_404,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import OrderForm
from .models import Order, Invoice
from profiles.models import Profile
from items.models import Item, ItemType
from django.contrib.sessions.backends.db import SessionStore
from django_countries.data import COUNTRIES
from django.template.loader import render_to_string
from django.core.mail import send_mail

import stripe


def order_create(request):

    # Initiate the Create Order form.
    account_type = request.user.profile.get_account_type()

    if account_type == 'Customer':
        messages.error(
            request,
            "Permission Denied : A customer cannot create an order")
        return redirect('menu')
    else:

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

        print("WHY AM I NOT A POST")
        # It is a get request from form so return an empty
        # form
        order_form = OrderForm()

        template = 'orders/order_create.html'
        context = {
            'order_form': order_form,
            'json_item_list': json_item_list,
            'json_order_list': json_order_list,
            'json_item_type_list': json_item_type_list,
        }

        return render(request, template, context)


def order_create_checkout(request):

    # Using a hosted payment page. Greater security provided
    # Check session data required
    local_key = get_order_form_data(request)
    storage_update = SessionStore(session_key=local_key)
    stripe_order = request.session["new_order"]
    stripe_order_id = request.session["new_order_id"]
    stripe_order_item_id = request.session["new_item_id"]
    stripe_order_profile_id = request.session['new_profile_id']
    stripe_line_item = (
        Item.objects.get(pk=stripe_order_item_id)
    )
    update_profile_stripe = Profile.objects.get(pk=stripe_order_profile_id)
    print((int(Decimal(stripe_order["cost_initial"])))*100)

    stripe_price = int(Decimal(stripe_order["cost_initial"]))*100
    stripe_ref = (
        f"{stripe_order["last_name"]}_{stripe_order_id}"
    )

    stripe.api_key = settings.STRIPE_SECRET_KEY

    if update_profile_stripe.stripe_id:
        stripe_customer = stripe.Customer.retrieve(
            update_profile_stripe.stripe_id)
        print("--- Stripe previous customer --- ")
        print(stripe_customer)
    else:
        stripe_customer = stripe.Customer.create(
            name=stripe_order["full_name"],
            email=stripe_order["email"],
            address={
                "line1": stripe_order["address_line_1"],
                "line2": stripe_order["address_line_2"],
                "city": stripe_order["town"],
                "state": stripe_order["county"],
                "postal_code": stripe_order["postcode"],
                "country": "GB"
            },
            shipping={
                "name": stripe_order["full_name"],
                "phone": stripe_order["phone_number"],
                "address": {
                    "line1": stripe_order["address_line_1"],
                    "line2": stripe_order["address_line_2"],
                    "city": stripe_order["town"],
                    "state": stripe_order["county"],
                    "postal_code": stripe_order["postcode"],
                    "country": "GB"
                }
            },
            phone=stripe_order["phone_number"]
        )

        update_profile_stripe.stripe_id = stripe_customer.id

        update_profile_stripe.save()
        print("--- Stripe new customer --- ")
        print(stripe_customer)
    # KEY HERE
    # ------------------------------------------------------

    # stripe_order = request.session["new_order"]
    # stripe_order_id = request.session["new_order_id"]
    # stripe_order_item_id = request.session["new_item_id"]
    # stripe_order_profile_id = request.session['new_profile_id']
    # These will be in a modal.
    stripe_success_url = (
        f"https://{request.META['HTTP_HOST']}"
        f"/orders/create/success/?session={local_key}")
    stripe_cancel_url = (
        f"https://{request.META['HTTP_HOST']}"
        f"/orders/create/cancel/?session={local_key}")
    stripe_image_url = (
        f"https://{request.META['HTTP_HOST']}"
        f"/media/{stripe_line_item.item_type.image}"
    )

    # print(f"SUCCESS URL : {stripe_success_url}")

    # price_data -> product_date is used to generate at runtime,
    # price would require the object to exist on Stripe
    # and so would price_data -> product

    # Tax Code : https://docs.stripe.com/tax/tax-codes?type=services

    checkout_session = stripe.checkout.Session.create(
        customer=stripe_customer.id,
        client_reference_id=stripe_ref,
        line_items=[{
            "price_data": {
                "currency": f"{settings.STRIPE_CURRENCY}",
                "product_data": {
                    "name": f"{stripe_line_item.item_type.name}",
                    "images": [stripe_image_url],
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

    storage_update["checkout_session"] = checkout_session.id
    storage_update.save()

    # As "request" is not the method used. It uses a GET with the return of the 
    # hosted payment page. This creates a session storage and posts the key to get in.
    # https://docs.djangoproject.com/en/5.1/topics/http/sessions/#using-sessions-out-of-views

    return redirect(checkout_session.url, code=303)


@csrf_exempt
def order_create_success(request):
    # Set your secret key.
    # See your keys here: https://dashboard.stripe.com/apikeys
    get_session = request.GET.get('session', '')

    if get_session == '':
        messages.error(
            request,
            "Could not get session data")
        return redirect('menu')
    else:

        retrieve_session = SessionStore(session_key=get_session)
        # stripe.api_key = settings.STRIPE_SECRET_KEY
        # stripe_session = stripe.checkout.Session.retrieve(
        #     retrieve_session["checkout_session"])

        # stripe_customer = stripe.Customer.retrieve(
        #     stripe_session.customer)
        get_item = Item.objects.get(pk=retrieve_session["new_item_id"])
        format_start_date = datetime.strptime(
            retrieve_session["new_order"]["start_date"],
            "%Y-%m-%d").date()
        format_end_date = datetime.strptime(
            retrieve_session["new_order"]["end_date"],
            "%Y-%m-%d").date()


        # https://www.geeksforgeeks.org/how-to-add-days-to-a-date-in-python/
        next_rental_date = format_start_date + timedelta(days=7)
        print(next_rental_date)

        if next_rental_date < format_end_date:
            # rental ends before next payment date
            next_payment = next_rental_date
        else:
            next_payment = None

        template = 'orders/order_create_success.html'
        context = {
            # 'stripe_session': stripe_session,
            # 'stripe_customer': stripe_customer,
            'item_ordered': get_item,
            'new_start_date': format_start_date,
            'new_end_date': format_end_date,
            'next_payment': next_payment,
            'order_form_data': retrieve_session["new_order"],
            "order_order_id": retrieve_session["new_order_id"],
            "order_profile_id": retrieve_session["new_profile_id"],
            "order_item_id": retrieve_session["new_item_id"],
            "order_invoice_id": retrieve_session["new_invoice_id"],
            'end_of_order': True,
        }
    send_confirmation_email(
        retrieve_session["new_order"],
        get_item,
        retrieve_session["new_order_id"],
        format_start_date,
        format_end_date,
        next_payment)

    return render(request, template, context)


@csrf_exempt
def order_create_cancel(request):
    # Set your secret key.
    # See your keys here: https://dashboard.stripe.com/apikeys
    get_session = request.GET.get('session', '')

    if get_session == '':
        messages.error(
            request,
            "Could not get session data")
        return redirect('menu')
    else:
        retrieve_session = SessionStore(session_key=get_session)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe_session = stripe.checkout.Session.retrieve(
            retrieve_session["checkout_session"])
        stripe_customer = stripe.Customer.retrieve(
            stripe_session.customer)
        print("ORDERCREATECANCEL")
        print("STRIPESESSION: ")
        print(stripe_session)
        print("CUSTOMERSESSION: ")
        print(stripe_customer)
        # print("LOCALSESSION:  ")
        # print(request.session['new_order'])
        template = 'orders/order_create_cancel.html'
        context = {
            'stripe_session': stripe_session,
            'stripe_customer': stripe_customer,
            'submitted_form_data': retrieve_session["new_order"],
            'end_of_order': True,
        }

    return render(request, template, context)


def get_order_form_data(request):

    session_store_data = SessionStore()

    form_data = {
        # Accordion - Customer
        # user_name will default null, unless order is created
        # from a historical customer. If an order and customer are
        # created at the same time it will need to create the User
        # and profile.
        'profile': request.POST['profile'],
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
        'country_name': COUNTRIES[request.POST['country']],
        'postcode': request.POST['postcode'],
        # Accordion - Order
        'item': request.POST['item'],
        'cost_initial': request.POST['cost_initial'],
        'cost_week': request.POST['cost_week'],
        'start_date': request.POST['start_date'],
        'end_date': request.POST['end_date'],
        # created_on: is done locally as datetime breaks json
        # and has no need to be transferred in form_data anywhere else
        'created_by': request.user.id,
        # Accordion - Payment
        'invoice_notes': request.POST['invoice_notes'],
    }

    print(" --- FORM DATA --- ")
    print(form_data)

    if form_data['profile'] == "None":

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

        # create because if it is found and update_or_create
        # is used, it will override the  default values.
        new_user, user_created = User.objects.get_or_create(
            first_name=form_data['first_name'],
            last_name=form_data['last_name'],
            email=form_data['email'],
            defaults={
                "is_superuser": False,
                "is_staff": False,
            }
        )

        print(" --- USER DATA --- ")
        print(f"Created? - {user_created} : {new_user}")
        # If it found a user it will check there is also no profile
        #
        # If it did not, it will create a new one because there cannot
        # be a profile without a user.

        # update_or_create is used, to keep the most up to date information
        # for someone where the first name, last name and email match.
        # In other words, should always retain the most up to date information
        # for the customer.
        new_profile, profile_created = Profile.objects.update_or_create(
            user=new_user,
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
        print(f"Created? - {profile_created} : {new_profile}")
        form_data['profile'] = new_profile.id
        # The "new_profile" profile object will be an instance of a
        # pre-existing or new user from these two queries.
        # print("Profile - From None")
        # print(new_profile)
    else:
        # print("Profile - From Form")
        new_profile = Profile.objects.get(pk=form_data['profile'])
        print(" --- EXISTING PEOFILE DATA FROM CUSTOMER PAGE --- ")
        print(new_profile)

    session_store_data["new_profile_id"] = new_profile.id
    
    # Create a model object from some of the form data and save()
    new_item = Item.objects.get(pk=form_data['item'])
    new_order = Order.objects.create(
        profile=new_profile,
        item=new_item,
        cost_initial=Decimal(form_data['cost_initial']),
        cost_week=Decimal(form_data['cost_week']),
        start_date=datetime.strptime(
            form_data['start_date'], '%Y-%m-%d'),
        end_date=datetime.strptime(
            form_data['end_date'], '%Y-%m-%d'),
        created_on=datetime.now(),
        created_by=request.user
    )

    new_order.save()
    print(" --- NEW ORDER DATA --- ")
    print(new_order)

    session_store_data["new_order_id"] = new_order.id
    session_store_data["new_item_id"] = new_item.id

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
        order=new_order,
        note=invoice_note_final,
        due_on=datetime.now(),
        amount_paid=Decimal(form_data['cost_initial']),
        status=0,
        stripe_pid='',
        created_on=datetime.now(),
        created_by=request.user
    )
    new_invoice.save()
    print(" --- NEW INVOICE DATA --- ")
    print(new_invoice)

    session_store_data["new_invoice_id"] = new_invoice.id
    session_store_data["new_order"] = form_data
    session_store_data.create()
    store_key = session_store_data.session_key

    return (store_key)


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


def send_confirmation_email(
        email_data, get_item, order_id,
        start_date, end_date, next_date):
    """
    Will accept different lengths with email_data.
    As long as it contains the fields it needs
    """
    address_line_list = [
        f"{email_data['address_line_2']}",
        f"{email_data['address_line_3']}",
        ]

    address_format = ""
    for x in address_line_list:
        if x == "":
            pass
        else:
            address_format += (x + "\n")

    email_data_format = {
        'order_id': order_id,
        'name': email_data["full_name"],
        'phone_number': email_data["phone_number"],
        'item': get_item.item_type.name,
        'category': get_item.item_type.category,
        'start_date': start_date.strftime("%d-%m-%Y"),
        'end_date': end_date.strftime("%d-%m-%Y"),
        'cost_initial': email_data["cost_initial"],
        'cost_week': email_data["cost_week"],
        'address_line_1': email_data["address_line_1"],
        'address_lines_23': address_format,
        'town': email_data["town"],
        'county': email_data["county"],
        'country': COUNTRIES[email_data["country"]],
        'postcode': email_data["postcode"]
    }

    subject = render_to_string(
        'emails/confirmation_emails/confirmation_email_subject.txt', {
            'email_data': email_data_format,
            'company_name': settings.COMPANY_NAME})
    body = render_to_string(
        'emails/confirmation_emails/confirmation_email_body.txt', {
            'email_data': email_data_format,
            'company_name': settings.COMPANY_NAME,
            'contact_email': settings.DEFAULT_FROM_EMAIL
        })

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [email_data["email"]]
    )
