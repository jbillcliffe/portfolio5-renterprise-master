from . import views
from django.urls import path
from .webhooks import webhook


"""
Path navigation for Item/ItemType
"""
urlpatterns = [
    path(
        'create/',
        views.order_create,
        name='order_create'),
    path(
        'cache_order_data/',
        views.cache_order_data,
        name='cache_order_data'),
    path('wh/', webhook, name='webhook')
]

# path('type/create/', views.item_type_create, name="item_type_create"),
# path('type/<int:id>/', views.item_type_view, name="item_type_view"),
