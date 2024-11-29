from django.shortcuts import render


def main_menu(request):
    """
    Function to display the main menu at the root
    of the project. Render a template, nothing more.
    """
    return render(request, 'menu/index.html')


def about_page(request):
    """
    Function to display the about page. 
    Render a template, nothing more.
    """
    return render(request, 'menu/about.html')
