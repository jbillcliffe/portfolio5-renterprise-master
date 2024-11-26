from . import views
from django.urls import path
from .webhooks import webhook


"""
Path navigation for Order/OrderNote/Invoice
"""
urlpatterns = [
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
    path('wh/', webhook, name='webhook')
]
