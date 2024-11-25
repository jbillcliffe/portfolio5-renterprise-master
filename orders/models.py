from django.db import models
from django.contrib.auth.models import User

from items.models import Item
from profiles.models import Profile

from datetime import date


# https://docs.djangoproject.com/en/5.1/topics/i18n/timezones/
# Store UTC, but interactions done with timezones (GMT/BST)
# Create your models here.
class Order(models.Model):
    # profile.user.first_name
    null_values = [None, 'None', 'none', 'null', 'Null']

    profile = models.ForeignKey(
        Profile, on_delete=models.PROTECT, related_name="order_profile"
    )
    item = models.ForeignKey(
        Item, on_delete=models.PROTECT, related_name="order_item"
    )
    cost_initial = models.DecimalField(max_digits=6, decimal_places=2)
    cost_week = models.DecimalField(max_digits=6, decimal_places=2)

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="order_created_by"
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"Order ID : {self.id}"

    def order_customer_name(self):
        if self.profile.user.first_name in self.null_values:
            return f"{self.profile.user.last_name}"
        else:
            return (
                f"{self.profile.user.first_name}"
                f" {self.profile.user.last_name}")

    def order_item_name(self):
        return self.item.item_type.name


class OrderNote(models.Model):

    null_values = [None, 'None', 'none', 'null', 'Null']

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order"
    )
    note = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="note_created_by"
    )

    class Meta:
        ordering = ["created_by"]
        verbose_name = "Order Note"
        verbose_name_plural = "Order Notes"

    def __str__(self):
        return f"Note for Order : {self.id}"

    def order_note_full_name(self):
        if self.order.profile.user.first_name in self.null_values:
            return f"{self.order.profile.user.last_name}"
        else:
            return (
                f"{self.order.profile.user.first_name}"
                f" {self.order.profile.user.last_name}")

    def created_on_by(self):
        return f"{self.created_on.strftime("%d-%m-%Y")}"


class Invoice(models.Model):

    # https://docs.djangoproject.com/en/5.1/ref/...
    # models/fields/#django.db.models.DateField.auto_now_add
    null_values = [None, 'None', 'none', 'null', 'Null']

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="invoice_order"
    )
    # USE_TZ in settings will be used, so it will use the timezone set
    # which is UTC for auto_now_add
    created_on = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="invoice_created_by"
    )
    # Different to created on, created on is the day it was done
    # But the due date could be different, although more often than not,
    # it is the date of creation.
    # Django docs states how auto_now_add cannot be overridden.
    # So date.today has a similar effect but can be changed.
    due_on = models.DateField(default=date.today)
    amount_paid = models.DecimalField(max_digits=6, decimal_places=2)
    note = models.TextField()
    status = models.BooleanField(default=False, verbose_name="Paid")
    stripe_pid = models.CharField(max_length=254, default='')

    # order by item_type name 0-9 then A-Z
    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Invoice ID : {self.id}"

    def invoice_name(self):
        if self.order.profile.user.first_name in self.null_values:
            return f"{self.order.profile.user.last_name}"
        else:
            return (
                f"{self.order.profile.user.first_name}"
                f" {self.order.profile.user.last_name}")
