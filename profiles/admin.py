from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from profiles.models import Profile, CustomerNote


"""
--- Django docs demonstrates how to extend the base user model ---
https://docs.djangoproject.com/en/5.1/topics/auth/customizing/

Through this admin.py , it removes the original User class by unregistering
it and then implementing a new UserAdmin class as an extension
of the User class. Ergo, instead of BaseUserAdmin class, it is now
BaseUserAdmin + the custom UserAdmin class.
"""


# https://docs.djangoproject.com/en/5.1/ref/contrib/admin/filters/#using-a-simplelistfilter
class ProfileListFilter(admin.SimpleListFilter):
    title = _("Profile Type")
    parameter_name = "Profile Type"

    def lookups(self, request, model_admin):
        return [
            ("customers", _("Customers")),
            ("staff", _("Staff")),
        ]

    def queryset(self, request, queryset):
        if self.value() == "customers":
            return queryset.filter(
                account_type=0
            )
        if self.value() == "staff":
            return queryset.filter(
                account_type__gt=0
            )


# Inline descriptor for Profile Model for the admin panel
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "profiles"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    can_delete = False
    verbose_name_plural = "profiles"
    list_filter = [ProfileListFilter]


class CustomerNoteAdmin(admin.ModelAdmin):
    model = CustomerNote
    verbose_name = "Customer Note"
    verbose_name_plural = "Customer Notes"


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(CustomerNote, CustomerNoteAdmin)
