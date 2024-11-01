from django.urls import path
from . import views


"""
Path navigation for user profiles.
"""


urlpatterns = [
    path('<pk:id>/', views.user_profile, name="user_profile"),
]
