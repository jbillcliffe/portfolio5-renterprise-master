from django.contrib import admin

from .models import Profile


# class UserAdminInline(admin.TabularInline):
#     model = User
#     fields = ('first_name', 'last_name', 'email',)


class ProfileAdmin(admin.ModelAdmin):
    # inlines = (UserAdminInline,)
    fields = (
        'address_line_1', 'address_line_2', 'address_line_3',
        'town', 'county', 'country', 'postcode', 'phone_number',
    )


admin.site.register(Profile, ProfileAdmin)
