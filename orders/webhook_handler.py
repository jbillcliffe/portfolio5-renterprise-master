from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, Invoice
from items.models import Item

from profiles.models import Profile

import json
import stripe
import time


class StripeWH_Handler:
    """
    Handle Stripe webhooks
    """

    def __init__(self, request):
        self.request = request

    # def _send_confirmation_email(self, order):
    #     """
    #     Send user a confirmation email
    #     """
    #     cust_email = order.email

    #     subject = render_to_string(
    #         'orders/confirmation_emails/confirmation_email_subject.txt',
    #         {'order': order})
    #     body = render_to_string(
    #         'checkout/confirmation_emails/confirmation_email_body.txt',
    #         {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

    #     send_mail(
    #         subject,
    #         body,
    #         settings.DEFAULT_FROM_EMAIL,
    #         [cust_email]
    #     )

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle a payment_intent.succeeded from Stripe
        """
        print("Intent Succeeded")
        intent = event.data.object
        # pid = intent.id

        # Get the Charge object
        # stripe_charge = stripe.Charge.retrieve(
        #     intent.latest_charge
        # )
        # print(stripe_charge)
        # billing_details = stripe_charge.billing_details  # updated
        # shipping_details = intent.shipping
        # grand_total = round(stripe_charge.amount / 100, 2)  # updated

        # Clean shipping details from stripe ("" not accepted, needs to be None)
        # for field, value in shipping_details.address.items():
        #     if value == "":
        #         shipping_details.address[field] = None

        # Update profile information if save_info was checked
        # Save the customer 
        # profile = None
        # username = intent.metadata.username
        # if username != 'AnonymousUser':
        #     profile = Profile.objects.get(user__username=username)
        #     if save_info:
        #         profile.default_phonephone_number = shipping_details.phone
        #         profile.default_country = shipping_details.address.country
        #         profile.default_postcode = shipping_details.address.postal_code
        #         profile.default_town_or_city = shipping_details.address.city
        #         profile.default_street_address1 = shipping_details.address.line1
        #         profile.default_street_address2 = shipping_details.address.line2
        #         profile.default_county = shipping_details.address.state
        #         profile.save()*/

        order_exists = False
        attempt = 1
        while attempt <= 5:
            # print("Attempt")
            # print(attempt)
            try:
                Invoice.objects.get(
                    # full_name__iexact=shipping_details.name,
                    stripe_pid__iexact=intent.stripe_pid
                )
                order_exists = True
                break
            except Invoice.DoesNotExist:
                attempt += 1
                time.sleep(1)
        print("Order Exists")

        if order_exists:
            # print("Point of first email")
            # self._send_confirmation_email(order)
            return HttpResponse(
                content=(
                    f'Webhook received: {event["type"]} |'
                    f'SUCCESS: Verified order already in database'),
                status=200)
        # else:
        #     order = None
        #     try:
        #         order = Order.objects.create(
        #             full_name=shipping_details.name,
        #             user_profile=profile,
        #             email=billing_details.email,
        #             phone_number=shipping_details.phone,
        #             country=shipping_details.address.country,
        #             postcode=shipping_details.address.postal_code,
        #             town_or_city=shipping_details.address.city,
        #             street_address1=shipping_details.address.line1,
        #             street_address2=shipping_details.address.line2,
        #             county=shipping_details.address.state,
        #             stripe_pid=pid,
        #         )
        #     except Exception as e:
        #         if order:
        #             order.delete()
        #         return HttpResponse(
        #             content=f'Webhook received: {event["type"]} | ERROR: {e}',
        #             status=500)

        # print("Point of 2nd email")
        # self._send_confirmation_email(order)
        # return HttpResponse(
        #         content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
        #         status=200)

    def handle_payment_intent_failed(self, event):
        """
        Handle a payment_intent.failed from Stripe
        """

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)