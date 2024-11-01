from django.urls import path
from . import views


"""
Path navigation for user profiles.
"""


urlpatterns = [
    # path('', views.profile_list, name="profile_list"),
    path('user/', views.profile, name="profile"),
]
