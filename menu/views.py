from django.shortcuts import render


def main_menu(request):
    """
    Function to display the main menu at the root
    of the project. Render a template, nothing more.
    """
    return render(request, 'menu/index.html')
