from django.conf import settings
"""
Context processor to return emails to template forms.
"""


# For Program related emails (contact/support etc.)
def system_emails(request):
    return {
        'HELP_EMAIL': settings.HELP_EMAIL,
        'FROM_EMAIL': settings.FROM_EMAIL
    }
