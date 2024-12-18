from . import views
from django.urls import path
from orders.views import (
    order_view, order_edit, order_create, customer_order_list)


"""
Path navigation for user profiles.
"""
urlpatterns = [
    path(
        '',
        views.ProfileList.as_view(),
        name='profile_list'),
    path(
        'user/',
        views.profile_view,
        name="profile_view"),
    path(
        'user/<int:user_id>/',
        views.profile_manage,
        name="profile_manage"),
    path(
        'create/',
        views.user_profile_create,
        {"is_customer": False},
        name="profile_create"),
    path(
        'customers/',
        views.customer_list,
        name='customer_list'),
    path(
        'customers/create/',
        views.customer_create,
        {"is_customer": True},
        name="customer_create"),
    path(
        'customers/<int:profile_id>/',
        views.customer_view,
        {"is_customer": True},
        name="customer_view"),
    path(
        'customers/<int:profile_id>/notes/',
        views.customer_notes,
        name="customer_notes"),
    path(
        'customers/<int:profile_id>/order/create/',
        order_create,
        name='customer_order_create',
    ),
    path(
        'customers/<int:profile_id>/orders/',
        customer_order_list,
        name='customer_order_list',
    ),
    path(
        'customers/<int:profile_id>/order/<int:order_id>/',
        order_view,
        name='order_view'),
    path(
        (
            'customers/<int:profile_id>/'
            'order/<int:order_id>/edit/<str:order_note>/'),
        order_edit,
        name='order_edit'),
]
