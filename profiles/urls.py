from . import views
from django.urls import path


"""
Path navigation for user profiles.
"""
urlpatterns = [
    path('', views.ProfileList.as_view(), name='profile_list'),
    path('user/', views.profile_view, name="profile_view"),
    path('user/<int:user_id>/', views.profile_manage, name="profile_manage"),
    path('customers/', views.customer_list, name='customer_list'),
]
