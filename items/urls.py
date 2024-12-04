from . import views
from django.urls import path


"""
Path navigation for Item/ItemType
"""
urlpatterns = [
    path(
        '',
        views.ItemList.as_view(),
        name='item_list'),
    path(
        '<int:item_id>/',
        views.item_view,
        name='item_view'),
    path(
        'create/',
        views.item_create,
        name='item_create'),
    path(
        'type/',
        views.ItemTypeList.as_view(),
        name='item_type_list'),
    path(
        'type/<int:type_id>/',
        views.item_type_view,
        name='item_type_view'),
    path(
        '<int:item_id>/type/<int:type_id>/edit/',
        views.item_type_update_inline,
        name='item_type_update_inline'),
    path(
        '<int:item_id>/status/',
        views.item_status_edit,
        name='item_status_edit'),
]

# path('type/create/', views.item_type_create, name="item_type_create"),
# path('type/<int:id>/', views.item_type_view, name="item_type_view"),
