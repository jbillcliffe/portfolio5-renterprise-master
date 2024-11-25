from . import views
from django.urls import path
# from .webhooks import webhook


"""
Path navigation for Order/OrderNote/Invoice
"""
urlpatterns = [
    path(
        'create/',
        views.order_create,
        name='order_create'),
    path(
        'order/create/success?session_id={CHECKOUT_SESSION_ID}',
        views.order_create_success,
        name="order_create_success")
]
