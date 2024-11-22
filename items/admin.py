from django.contrib import admin
from .models import Item, ItemType


class ItemTypeAdmin(admin.ModelAdmin):
    model = ItemType
    can_delete = False
    verbose_name_plural = "Item Types"
    list_display = ('name',)


class ItemAdmin(admin.ModelAdmin):
    model = Item
    verbose_name_plural = "Items"


admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(Item, ItemAdmin)
