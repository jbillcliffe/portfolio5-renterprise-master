from . import views
from django.urls import path


"""
Path navigation for Order/OrderNote/Invoice
"""
urlpatterns = [
    path(
        '',
        views.OrderList.as_view(),
        name='order_list'),
    path(
        'create/',
        views.order_create,
        name='order_create'),
    path(
        'create/checkout/',
        views.order_create_checkout,
        name='order_create_checkout'),
    path(
        'create/success/',
        views.order_create_success,
        name="order_create_success"),
    path(
        'create/cancel/',
        views.order_create_cancel,
        name="order_create_cancel"),
    path(
        'payment/checkout/<int:invoice_id>/',
        views.payment_create,
        name='payment_create'),
    path(
        'payment/success/',
        views.payment_success,
        name="payment_success"),
    path(
        'payment/cancel/',
        views.payment_cancel,
        name="payment_cancel"),
    # Order View is reached through a customer.
    # It appears in the profiles
]
