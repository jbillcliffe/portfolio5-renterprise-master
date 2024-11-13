from . import views
from django.urls import path


"""
Path navigation for user profiles.
"""
urlpatterns = [
    path('', views.ItemList.as_view(), name='item_list'),
    path('<int:item_id>/', views.item_view, name="item_view"),
]

# path('create/', views.item_create, name="item_create"),
# path('type/create/', views.item_type_create, name="item_type_create"),
# path('type/<int:id>/', views.item_type_view, name="item_type_view"),
