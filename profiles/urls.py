from django.urls import path
from . import views


"""
- URLs relating to profile navigation.
- Such as profile view, edit details, change password.
"""


urlpatterns = [
    path('', views.main_menu, name="menu"),
]
