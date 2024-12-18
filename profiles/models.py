from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
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
class Profile(models.Model):
    """
    - A user profile to keep important details in regards to the account.
    - The user profile, is an extension of the User class.
    - If someone is staff/admin/hr, their address will need to be here. But
    not for a customer, as their details are held by the Customer app.
    - Set default to be customer. This will mean they have no access
    to many things. A staff member/admin/super user will be able to
     update their account type.
    """

    # Human readable values for int values relating to the account type
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
    account_type = models.IntegerField(
        choices=ACCOUNT_TYPE, default=CUSTOMER
    )
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
        max_length=50, null=True, blank=True, choices=GB_REGION_CHOICES
    )
    country = CountryField(
        blank_label='Country', null=True, blank=True, default="GB"
    )
    postcode = models.CharField(
        max_length=20, null=True, blank=True
    )
    phone_number = models.CharField(
        max_length=20, null=True, blank=True
    )
    stripe_id = models.CharField(
        max_length=254, null=True, blank=True, default=''
    )

    # Ordering alphabetically by last name from the User Model
    class Meta:
        ordering = ["user__last_name"]

    # Visual representation of this model is the username
    def __str__(self):
        return self.user.username

    def get_account_type(self):
        """
        Returning the human readable version of ACCOUNT_TYPE
        """
        return self.ACCOUNT_TYPE[self.account_type][1]

    def get_last_name(self):
        """
        Returning the last_name which is stored in the User
        """
        return self.user.last_name

    def get_full_name(self):
        """
        Self contained function to get first and last name by
        calling a function and relating it to the NULL_VALUES in the settings
        """
        if self.user.first_name in settings.NULL_VALUES:
            return f"{self.user.last_name}"
        else:
            return f"{self.user.first_name} {self.user.last_name}"

    def address_display(self):
        return f"{self.address_line_1}, {self.county}, {self.postcode}"


class CustomerNote(models.Model):

    null_values = [None, 'None', 'none', 'null', 'Null']

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="profile"
    )
    note = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="customer_note_created_by"
    )

    class Meta:
        ordering = ["created_by"]
        verbose_name = "Customer Note"
        verbose_name_plural = "Customer Notes"

    def __str__(self):
        return f"Note for Customer : {self.profile.id}"

    def customer_note_full_name(self):
        if self.profile.user.first_name in self.null_values:
            return f"{self.profile.user.last_name}"
        else:
            return (
                f"{self.profile.user.first_name}"
                f" {self.profile.user.last_name}")
