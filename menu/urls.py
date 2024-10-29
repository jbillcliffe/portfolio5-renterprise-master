from django.urls import path
from . import views


"""
--- CREDIT TO PORTFOLIO 4 :
    https://github.com/jbillcliffe/django-renterprise/blob/main/menu/urls.py

URLs relating to menu navigation
- Contains URLs for the buttons on the main menu to navigate
the rest of the program
- This is the root page for the project.
"""


urlpatterns = [
    path('', views.main_menu, name="menu"),
]
