from . import views
from django.urls import path


"""
Path navigation for Item/ItemType
"""
urlpatterns = [
    path(
        'create/',
        views.order_create,
        name='order_create'),
]

# path('type/create/', views.item_type_create, name="item_type_create"),
# path('type/<int:id>/', views.item_type_view, name="item_type_view"),
