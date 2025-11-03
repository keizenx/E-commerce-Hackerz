"""
URLs pour la wishlist
"""
from django.urls import path
from . import views_wishlist

app_name = 'wishlist'

urlpatterns = [
    path('', views_wishlist.wishlist_view, name='view'),
    path('add/<int:product_id>/', views_wishlist.add_to_wishlist, name='add'),
    path('remove/<int:product_id>/', views_wishlist.remove_from_wishlist, name='remove'),
    path('toggle/<int:product_id>/', views_wishlist.toggle_wishlist, name='toggle'),
    path('clear/', views_wishlist.clear_wishlist, name='clear'),
]
