from django.shortcuts import render
import os


def index(request):
    """
    Function to display the main menu at the root
    of the project. Render a template, nothing more.
    """
    print(os.environ)
    return render(request, 'menu/index.html')


def about_page(request):
    """
    Function to display the about page.
    Render a template, nothing more.
    """
    return render(request, 'menu/about.html')