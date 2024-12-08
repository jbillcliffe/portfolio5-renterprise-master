from datetime import datetime, timedelta
from decimal import Decimal
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from .forms import (
    OrderForm, OrderDatesForm,
    OrderItemForm, OrderNoteForm)
from .models import Order, Invoice, OrderNote
from items.models import Item, ItemType
from profiles.models import Profile

from django_countries.data import COUNTRIES
from urllib.parse import urlencode
import stripe


@method_decorator(login_required, name='dispatch')
class OrderList(ListView):
    """
    Class ListView to display the orders into a table.
    """
    paginate_by = 7
    model = Order
    template_name = 'orders/order_list.html'

    def get_context_data(self, **kwargs):
        context = super(OrderList, self).get_context_data(**kwargs)
        return context


@login_required
def customer_order_list(request, profile_id):
    # Build query, users with account type 0 are customers.

    # Also want to include any profiles on an order otherwise. Staff members
    # can be a customer too if they make an order. So they would not have an
    # "account_type" of 0 So best method is to get an iterable of
    # "profile ids" from the Orders model. To then get profile objects
    # https://docs.djangoproject.com/en/5.1/ref/models/querysets/#in

    # Found list of foreign key object query :
    # https://stackoverflow.com/questions/45062238/django-getting-a-list-of-foreign-key-objects
    # Immediately takes the query result (list of profiles from Order) and
    # searches them using an IN query to get out Profile objects.

    # Complex query, was initially a Union query. But that was not merging
    # together eg. Would want 1,3,5 and 2,4,6 to become 1,2,3,4,5,6.
    # Instead the generated queryset would be 1,3,5,2,4,6. So this uses an OR
    # statement, which makes sense given that it is querying the same model
    # but in differnet ways. First - It looks at where the iterated Profile
    # in the query, appears in the Order model as a foreign key.
    # Then it simply gets accounts which have an account_type of 0.

    customer_order_queryset = Order.objects.filter(profile=profile_id)

    # 7 results per page

    orders = Paginator(customer_order_queryset, 7)

    # Determine number of pages in query
    page_number = request.GET.get("page")
    page_obj = orders.get_page(page_number)

    return render(
        request, "customers/customer_order_list.html",
        {"page_obj": page_obj, "profile_id": profile_id})


def order_view(request, profile_id, order_id):

    order = Order.objects.get(
        pk=order_id,
        profile=profile_id
    )
    item_id = order.item.id
    item = Item.objects.get(id=item_id)

    invoices = Invoice.objects.filter(order__id=order_id)
    dates_form = OrderDatesForm(instance=order)
    item_form = OrderItemForm(instance=item)
    order_note_form = OrderNoteForm()
    invoice_list = Paginator(invoices, 5)

    # Determine number of pages in query
    page_number = request.GET.get("page")
    page_obj = invoice_list.get_page(page_number)

    order_notes = OrderNote.objects.filter(order=order_id)
    order_notes_list = Paginator(order_notes, 5)
    # Determine number of pages in query
    page_number_extra = request.GET.get("page-extra")
    page_obj_extra = order_notes_list.get_page(page_number_extra)
    
    if request.user.profile.get_account_type == 'Customer':
        json_item_list = ""
        json_item_type_list = ""
        json_order_list = ""
    else:
        json_item_list = serialize(
            'json', Item.objects.all(),
            fields=[
                "item_type", "repair_date",
                "income", "status"],
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

        if request.POST.get('tab'):
            tab_return = request.POST.get('tab')
        else:
            tab_return = None

    account_type = request.user.profile.get_account_type()

    template = 'orders/order_view.html'
    context = {
        # 'order_view_form': order_view_form,
        'order': order,
        'account_type': account_type,
        'tab_return': tab_return,
        'order_dates_form': dates_form,
        'order_item_form': item_form,
        'order_note_form': order_note_form,
        'profile_id': profile_id,
        # 'item_type'
        # 'profile'
        'json_item_list': json_item_list,
        'json_order_list': json_order_list,
        'json_item_type_list': json_item_type_list,
        "page_obj": page_obj,
        "page_obj_extra": page_obj_extra,
    }

    return render(request, template, context)


def order_edit(request, profile_id, order_id, order_note):

    account_type = request.user.profile.get_account_type()
    get_order = Order.objects.get(pk=order_id)
    print(account_type)

    if account_type == "Customer":
        messages.error(
            request,
            "Permission Denied : A customer cannot modify an order")
    else:
        print(request.POST)
        if request.method == "POST":

            tab_return = request.GET['tab']
            
            if tab_return == "notes":
                print(request.POST)

                new_order_note = OrderNote.objects.create(
                    note=request.POST['note'],
                    order=get_order,
                    created_by=request.user,
                    created_on=datetime.now())
                new_order_note.save()

                print(new_order_note.id)
                print(new_order_note.note)
                print(new_order_note.created_by)

                messages.success(
                    request,
                    ("A new order note has been created")
                )

                url = reverse('order_view', args=[profile_id, order_id])
                query = urlencode({'tab': tab_return})
                final_url = '{}?{}'.format(url, query)
                return redirect(final_url)

            elif tab_return == "despatches":
                print("GOT TAB")
                form = OrderDatesForm(request.POST, instance=get_order)
                form.save()

                save_order_note = OrderNote.objects.create(
                    order=get_order,
                    note=order_note,
                    created_on=datetime.now(),
                    created_by=request.user
                )
                save_order_note.save()
                print("saved stuff")
                messages.success(
                    request,
                    "Order Edited : Date(s) changed for this order")

                url = reverse('order_view', args=[profile_id, order_id])
                query = urlencode({'tab': tab_return})
                final_url = '{}?{}'.format(url, query)

                return redirect(final_url)
            else:
                messages.error(
                    request,
                    (
                        "Order Edit Failed : There was a problem "
                        "with the operation. Please contact your IT "
                        "Administrator"))
                return redirect(
                    reverse('order_view', args=[profile_id, order_id]))
        else:
            if request.GET['tab'] == "payments":
                invoice_id = request.GET['invoice']
                status = request.GET['status']

                print(status)
                print(invoice_id)

                if status == "unpaid":
                    invoice = Invoice.objects.get(pk=invoice_id)
                    invoice.status = False
                    invoice.save()

                    save_order_note = OrderNote.objects.create(
                        order=get_order,
                        note=f"Invoice {invoice_id} marked as unpaid",
                        created_on=datetime.now(),
                        created_by=request.user
                    )
                    save_order_note.save()

                    messages.warning(
                        request,
                        (
                            f"INVOICE UNPAID : {invoice_id} has"
                            f" been been marked as unpaid!"
                        )
                    )
                    print("UNPAID")
                elif status == "paid":
                    invoice = Invoice.objects.get(pk=invoice_id)
                    invoice.status = True
                    invoice.save()

                    save_order_note = OrderNote.objects.create(
                        order=get_order,
                        note=f"Invoice {invoice_id} marked as paid",
                        created_on=datetime.now(),
                        created_by=request.user
                    )
                    save_order_note.save()

                    messages.success(
                        request,
                        (
                            f"INVOICE PAID : {invoice_id} has"
                            f" been been marked as paid!"
                        )
                    )
                    print("PAID")
                elif status == "deleted":
                    invoice = Invoice.objects.get(pk=invoice_id)
                    invoice.delete()

                    save_order_note = OrderNote.objects.create(
                        order=get_order,
                        note=f"INVOICE {invoice_id} DELETED",
                        created_on=datetime.now(),
                        created_by=request.user
                    )
                    save_order_note.save()

                    messages.warning(
                        request,
                        f"INVOICE DELETED : {invoice_id} has been deleted!"
                    )
                    print("DELETED")
                else:
                    # error message
                    messages.error(
                        request,
                        (
                            "INVOICE ERROR : Unknown invoice operation. "
                            "Show this URL to IT support."
                        )
                    )
                url = reverse('order_view', args=[profile_id, order_id])
                query = urlencode({'tab': request.GET['tab']})
                final_url = '{}?{}'.format(url, query)

                return redirect(final_url)


@login_required
def order_create(request, profile_id=None):
    # Initiate the Create Order form.
    account_type = request.user.profile.get_account_type()

    if account_type == 'Customer':
        messages.error(
            request,
            "Permission Denied : A customer cannot create an order")
        return redirect('menu')
    else:
        if profile_id:
            order_form = OrderForm(profile_id=profile_id)
        else:
            order_form = OrderForm(profile_id=None)

        json_item_list = serialize(
            'json', Item.objects.all(),
            fields=[
                "item_type", "repair_date",
                "income", "status"],
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

        template = 'orders/order_create.html'
        context = {
            'order_form': order_form,
            'json_item_list': json_item_list,
            'json_order_list': json_order_list,
            'json_item_type_list': json_item_type_list,
            'profile_id': profile_id,
        }

        return render(request, template, context)


@login_required
def payment_create(request, invoice_id):

    session_store_data = SessionStore()
    session_store_data.create()
    store_key = session_store_data.session_key
    get_invoice = Invoice.objects.get(pk=invoice_id)
    stripe_invoice_id = get_invoice.id
    stripe_order_id = get_invoice.order
    stripe_profile = get_invoice.order.profile
    stripe_line_item = get_invoice.order.item.item_type
    stripe_price = int(Decimal(get_invoice.amount_paid))*100
    stripe_ref = (
        f"{stripe_profile.user.last_name}_{stripe_order_id}"
    )
    stripe.api_key = settings.STRIPE_SECRET_KEY

    if stripe_profile.stripe_id:
        stripe_customer = stripe.Customer.retrieve(
            stripe_profile.stripe_id)
        print("--- Stripe previous customer --- ")
        print(stripe_customer)
    else:
        stripe_customer = stripe.Customer.create(
            name=stripe_profile.get_full_name,
            email=stripe_profile.user.email,
            address={
                "line1": stripe_profile.address_line_1,
                "line2": stripe_profile.address_line_2,
                "city": stripe_profile.town,
                "state": stripe_profile.county,
                "postal_code": stripe_profile.postcode,
                "country": "GB"
            },
            shipping={
                "name": stripe_profile.get_full_name,
                "phone": stripe_profile.phone_number,
                "address": {
                    "line1": stripe_profile.address_line_1,
                    "line2": stripe_profile.address_line_2,
                    "city": stripe_profile.town,
                    "state": stripe_profile.county,
                    "postal_code": stripe_profile.postcode,
                    "country": "GB"
                }
            },
            phone=stripe_profile.phone_number
        )

        stripe_profile.stripe_id = stripe_customer.id

        stripe_profile.save()
        print("--- Stripe new customer --- ")
        print(stripe_customer)

    stripe_success_url = (
        f"https://{request.META['HTTP_HOST']}"
        f"/orders/payment/success/?session={store_key}")
    stripe_cancel_url = (
        f"https://{request.META['HTTP_HOST']}"
        f"/orders/payment/cancel/?session={store_key}")
    stripe_image_url = (
        f"https://{request.META['HTTP_HOST']}"
        f"/media/{stripe_line_item.image}"
    )

    if stripe_line_item.product_stripe_id:
        created_line_items_array = [{
            "price": f"{stripe_line_item.product_stripe_id}",
            "quantity": 1
        }]
    else:
        created_line_items_array = [{
            "price_data": {
                "currency": f"{settings.STRIPE_CURRENCY}",
                "product_data": {
                    "name": f"{stripe_line_item.name}",
                    "images": [stripe_image_url],
                    "tax_code": "txcd_20030000"
                },
                "tax_behavior": "exclusive",
                "unit_amount": stripe_price
            },
            "quantity": 1
        }]
    checkout_session = stripe.checkout.Session.create(
        customer=stripe_customer.id,
        client_reference_id=stripe_ref,
        line_items=created_line_items_array,
        mode="payment",
        success_url=stripe_success_url,
        cancel_url=stripe_cancel_url,
        payment_intent_data={"setup_future_usage": "off_session"}
    )

    session_store_data["checkout_session"] = checkout_session.id
    session_store_data["invoice_id"] = stripe_invoice_id
    session_store_data["order_id"] = stripe_order_id.id
    session_store_data["customer_id"] = stripe_profile.id
    session_store_data["amount_paid"] = str(get_invoice.amount_paid)
    session_store_data.save()

    # As "request" is not the method used. It uses a GET with the return of
    # the hosted payment page. This creates a session storage and posts the
    # key to get in.
    # https://docs.djangoproject.com/en/5.1/topics/http/sessions/#using-sessions-out-of-views
    return redirect(checkout_session.url, code=303)


@csrf_exempt
@login_required
def payment_success(request):
    # Set your secret key.
    # See your keys here: https://dashboard.stripe.com/apikeys
    get_session = request.GET.get('session', '')
    # Two parts need to happen at this point to reflect the successful payment
    #
    # - The invoice needs to be set to paid
    # - The item needs to have the income added to it.
    #
    # It can only do this with the session data. But it also cannot do it
    # before this function, because the payment could still be unsuccessful.
    if get_session == '':
        messages.error(
            request,
            "Could not get session data")
        return redirect('menu')
    else:
        retrieve_session = SessionStore(session_key=get_session)
        template = 'orders/payments/payment_success.html'
        order_get = Order.objects.get(pk=retrieve_session["order_id"])

        invoice = Invoice.objects.get(pk=retrieve_session["invoice_id"])
        invoice.status = True
        invoice.save()

        ordernote = OrderNote.objects.create(
            order=order_get,
            created_by=request.user,
            note=f"Payment for Invoice {invoice.id} complete."
        )
        ordernote.save()

        context = {
            'invoice': invoice,
            'order': order_get,
        }
    send_payment_email(
        retrieve_session["invoice_id"],
        retrieve_session["order_id"],
        retrieve_session["customer_id"]
    )
    # Remove this order/stripe session after payment and email for the user
    # It has pulled out all the data it requires.
    retrieve_session.delete(get_session)
    return render(request, template, context)


@csrf_exempt
@login_required
def payment_cancel(request):
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
        template = 'orders/payments/payment_cancel.html'
        context = {
            'stripe_session': stripe_session,
            'stripe_customer': stripe_customer,
        }

    return render(request, template, context)


@login_required
def order_create_checkout(request):

    # Using a hosted payment page. Greater security provided
    # Check session data required
    local_key = get_order_form_data(request)
    print("KEY")
    print(local_key)
    storage_update = SessionStore(session_key=local_key)
    stripe_order = storage_update["new_order"]
    stripe_order_id = storage_update["new_order_id"]
    stripe_order_item_id = storage_update["new_item_id"]
    stripe_order_profile_id = storage_update['new_profile_id']
    stripe_line_item = (
        Item.objects.get(pk=stripe_order_item_id)
    )
    update_profile_stripe = Profile.objects.get(pk=stripe_order_profile_id)

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

    # As "request" is not the method used. It uses a GET with the
    # return of the hosted payment page. This creates a session storage
    # and posts the key to get in.
    # https://docs.djangoproject.com/en/5.1/topics/http/sessions/#using-sessions-out-of-views

    return redirect(checkout_session.url, code=303)


@csrf_exempt
@login_required
def order_create_success(request):
    # Set your secret key.
    # See your keys here: https://dashboard.stripe.com/apikeys
    get_session = request.GET.get('session', '')
    # Two parts need to happen at this point to reflect the successful payment
    #
    # - The invoice needs to be set to paid
    # - The item needs to have the income added to it.
    #
    # It can only do this with the session data. But it also cannot do it
    # before this function, because the payment could still be unsuccessful.

    if get_session == '':
        messages.error(
            request,
            "Could not get session data")
        return redirect('menu')
    else:

        retrieve_session = SessionStore(session_key=get_session)
        get_item = Item.objects.get(pk=retrieve_session["new_item_id"])
        format_start_date = datetime.strptime(
            retrieve_session["new_order"]["start_date"],
            "%Y-%m-%d").date()
        format_end_date = datetime.strptime(
            retrieve_session["new_order"]["end_date"],
            "%Y-%m-%d").date()
        print(f"pre income add : {Decimal(get_item.income)}")
        print(
            f"pre income add cost: "
            f"{Decimal(retrieve_session["new_order"]["cost_initial"])}")
        trace_test = (
            Decimal(get_item.income) +
            Decimal(retrieve_session["new_order"]["cost_initial"]))
        print(trace_test)
        print(f"post income add : {trace_test}")

        # https://www.geeksforgeeks.org/how-to-add-days-to-a-date-in-python/
        next_rental_date = format_start_date + timedelta(days=7)

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
    # Remove this order/stripe session after payment and email for the user
    # It has pulled out all the data it requires.
    retrieve_session.delete(get_session)
    return render(request, template, context)


@csrf_exempt
@login_required
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


@login_required
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
        'postcode': request.POST['postcode'],
        # Accordion - Order
        'item': request.POST['item'],
        'cost_initial': request.POST['cost_initial'],
        'cost_week': request.POST['cost_week'],
        'start_date': request.POST['start_date'],
        'end_date': request.POST['end_date'],
        # created_on: is done locally as datetime breaks json
        # and has no need to be transferred in form_data anywhere else
        'created_by': str(request.user.id),
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
        invoice_note_list.append(form_data['invoice_notes'])
    invoice_note_final = ' '.join(invoice_note_list)
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
            'contact_email': settings.INFO_EMAIL
        })

    send_mail(
        subject,
        body,
        settings.INFO_EMAIL,
        [email_data["email"]]
    )


def send_payment_email(
        invoice_id, order_id, customer_id):
    """
    Will accept different lengths with email_data.
    As long as it contains the fields it needs
    """

    get_customer = Profile.objects.get(pk=customer_id)
    get_invoice = Invoice.objects.get(pk=invoice_id)

    email_data_format = {
        'order_id': order_id,
        'name': get_customer.get_full_name,
        'amount_paid': get_invoice.amount_paid,
        'invoice': get_invoice.id
    }

    subject = render_to_string(
        'emails/payment_emails/payment_email_subject.txt', {
            'email_data': email_data_format,
            'company_name': settings.COMPANY_NAME})
    body = render_to_string(
        'emails/payment_emails/payment_email_body.txt', {
            'email_data': email_data_format,
            'company_name': settings.COMPANY_NAME,
            'contact_email': settings.INFO_EMAIL
        })

    send_mail(
        subject,
        body,
        settings.INFO_EMAIL,
        [get_customer.user.email]
    )
