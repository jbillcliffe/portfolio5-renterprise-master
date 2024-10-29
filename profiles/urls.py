from django.urls import path
from . import views


"""
- URLs relating to profile navigation.
- Such as profile view, edit details, change password.
"""


urlpatterns = [
    path('', views.profile_list, name="profile_list"),
]
