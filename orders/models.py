from django.db import models
from django.contrib.auth.models import User

from items.models import Item
from profiles.models import Profile


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
    end_date = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="order_created_by"
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"Order ID : {self.id} - {self.profile.user.last_name}"

    def order_customer_name(self):
        if self.profile.user.first_name in self.null_values:
            return f"{self.profile.user.last_name}"
        else:
            return (
                f"{self.profile.user.first_name}"
                f" {self.profile.user.last_name}")

    def order_item_name(self):
        return f"{self.item.item_type.name}"


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

    def __str__(self):
        return f"{self.id}"

    def order_note_full_name(self):
        if self.order.profile.user.first_name in self.null_values:
            return f"{self.order.profile.user.last_name}"
        else:
            return (
                f"{self.order.profile.user.first_name}"
                f" {self.order.customer.last_name}")

    def created_on_by(self):
        return f"{self.created_on.strftime("%d-%m-%Y")}"


class Invoice(models.Model):

    null_values = [None, 'None', 'none', 'null', 'Null']

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="invoice_order"
    )
    created_on = models.DateField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=6, decimal_places=2)
    note = models.TextField()
    status = models.BooleanField(default=False)

    # order by item_type name 0-9 then A-Z
    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Invoice ID : {self.id}"

    def invoice_customer_name(self):
        if self.order.customer.first_name in self.null_values:
            return f"{self.order.customer.last_name}"
        else:
            return (
                f"{self.order.customer.first_name}"
                f" {self.order.customer.last_name}")
