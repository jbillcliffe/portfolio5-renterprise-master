from django import template
# https://www.geeksforgeeks.org/concatenate-strings-in-django-templates/

register = template.Library()


@register.filter
def xml_url(location, file):
    """Concatenate value and arg."""
    return {
        "location": location,
        "file": file
    }
