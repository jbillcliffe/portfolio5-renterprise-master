from django.db import models
from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver

from django_countries.fields import CountryField
from localflavor.gb.gb_regions import GB_REGION_CHOICES

"""
Profiles Model
--------------------------------
Inspiration from Boutique Ado tutorial :
https://github.com/Code-Institute-Solutions/boutique_ado_v1
--------------------------------
Use of django-localflavor (Counties) referenced from previous project
https://github.com/jbillcliffe/django-renterprise
--------------------------------
- A place to hold additional data for a user.
- Such as address and contact details.
- Also needs to define them as a customer, staff, admin or hr.
- Depending on profile type will determine their access.
"""


# Create your models here.
class UserProfile(models.Model):
    """
    - A user profile to keep important details in regards to the account.
    - The user profile, is an extension of the User class.
    - If someone is staff/admin/hr, their address will need to be here. But
    not for a customer, as their details are held by the Customer app.
    """

    CUSTOMER = 0
    STAFF = 1
    HR = 2
    ADMINISTRATOR = 3
    ACCOUNT_TYPE = (
        (CUSTOMER, 'Customer'),
        (STAFF, 'Staff'),
        (HR, 'HR'),
        (ADMINISTRATOR, 'Administrator'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_line_1 = models.CharField(
        max_length=80, null=True, blank=True
    )
    address_line_2 = models.CharField(
        max_length=80, null=True, blank=True
    )
    address_line_3 = models.CharField(
        max_length=80, null=True, blank=True
    )
    town = models.CharField(
        max_length=40, null=True, blank=True
    )
    county = models.CharField(
        choices=GB_REGION_CHOICES
    )
    country = CountryField(
        blank_label='Country', null=True, blank=True
    )
    postcode = models.CharField(
        max_length=20, null=True, blank=True
    )
    phone_number = models.CharField(
        max_length=20, null=True, blank=True
    )

    def __str__(self):
        return self.user.username


# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     """
#     Create or update user profile
#     """
#     if created:
#         UserProfile.objects.create(user=instance)
#     # Existing user will just save profile
#     instance.userprofile.save()