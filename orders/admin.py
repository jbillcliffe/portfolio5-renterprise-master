from django.contrib import admin
from .models import Order, OrderNote, Invoice


# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    model = Order
    can_delete = False
    verbose_name_plural = "Orders"
    list_display = (
        'id', 'profile', 'order_item_name',
        'start_date', 'end_date')


class OrderNoteAdmin(admin.ModelAdmin):
    model = OrderNote
    can_delete = False
    verbose_name_plural = "Order Notes"
    list_display = ('order', 'created_on', 'created_by')


class InvoiceAdmin(admin.ModelAdmin):
    model = Invoice
    can_delete = False
    verbose_name_plural = "Invoices"
    list_display = (
        'id', 'due_on', 'order', 'created_on', 'amount_paid',
        'status')


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderNote, OrderNoteAdmin)
admin.site.register(Invoice, InvoiceAdmin)
