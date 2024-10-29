from django.contrib import admin
from django.contrib.auth.models import User

from .models import Profile


# class UserAdminInline(admin.TabularInline):
#   model = User
#   fields = ('first_name', 'last_name', 'email',)


class ProfileAdmin(admin.ModelAdmin):
    # inlines = (UserAdminInline,)
    fields = (
        'user', 'address_line_1', 'address_line_2', 'address_line_3',
        'town', 'county', 'country', 'postcode', 'phone_number',
        'account_type', 
    )


admin.site.register(Profile, ProfileAdmin)
