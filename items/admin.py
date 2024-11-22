from django.contrib import admin
from .models import Item, ItemType


class ItemTypeAdmin(admin.ModelAdmin):
    model = ItemType
    can_delete = False
    verbose_name_plural = "item types"
    list_display = ('name',)


class ItemAdmin(admin.ModelAdmin):
    model = Item
    verbose_name_plural = "items"


admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(Item, ItemAdmin)
