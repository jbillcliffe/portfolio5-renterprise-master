from . import views
from django.urls import path
from orders.views import order_view, order_edit


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
        'customers/<int:profile_id>/',
        views.customer_view,
        name="customer_view"),
    path(
        'customers/create/',
        views.user_profile_create,
        {"is_customer": True},
        name="customer_create"),
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
