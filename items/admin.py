from django.contrib import admin
from .models import Item, ItemType


class ItemTypeAdmin(ItemType):
    model = ItemType
    can_delete = False
    verbose_name_plural = "item types"
    list_display = ('name',)


class ItemAdmin(Item):
    model = Item
    verbose_name_plural = "items"


admin.register(ItemTypeAdmin, ItemAdmin)
