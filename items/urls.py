from . import views
from django.urls import path


"""
Path navigation for user profiles.
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
        '<int:item_id>/type/<int:type_id>/edit',
        views.item_type_update_inline,
        name='item_type_update_inline')
]

# path('create/', views.item_create, name="item_create"),
# path('type/create/', views.item_type_create, name="item_type_create"),
# path('type/<int:id>/', views.item_type_view, name="item_type_view"),
