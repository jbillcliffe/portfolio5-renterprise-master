from django.conf import settings
"""
Context processor to return company variables to template forms.
"""


# For Program related emails (contact/support etc.)
def settings_variables(request):
    return {
        'COMPANY_NAME': settings.COMPANY_NAME,
        'HELP_EMAIL': settings.HELP_EMAIL,
        'INFO_EMAIL': settings.INFO_EMAIL,
        'BASIC_INFO_EMAIL': settings.BASIC_INFO_EMAIL,
        'BASIC_HELP_EMAIL': settings.BASIC_HELP_EMAIL,
        'COMPANY_PHONE': settings.COMPANY_PHONE,
        'COMPANY_HELP_PHONE': settings.COMPANY_HELP_PHONE,
        'COMPANY_ADDRESS': settings.COMPANY_ADDRESS,
        # 'XML_LOCATION': settings.XML_LOCATION,
    }
