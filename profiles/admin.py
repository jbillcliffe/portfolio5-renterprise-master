from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from profiles.models import Profile


"""
--- Django docs demonstrates how to extend the base user model ---
https://docs.djangoproject.com/en/5.1/topics/auth/customizing/

Through this admin.py , it removes the original User class by unregistering
it and then implementing a new UserAdmin class as an extension
of the User class. Ergo, instead of BaseUserAdmin class, it is now
BaseUserAdmin + the custom UserAdmin class.
"""


# Inline descriptor for Profile Model for the admin panel
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "profiles"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
