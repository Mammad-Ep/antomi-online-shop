from django.urls import path
from .views import *
# _________________________________________________________________

app_name = 'favorites'

urlpatterns = [
    path('add_favorite_product/', add_favorite_product, name='add_favorite_product'),
    path('remove_favorite_product/', remove_favorite_product, name='remove_favorite_product'),
    path('wishlist/', Wishlist.as_view(), name='wishlist'),
    path('show_wishlist/', show_wishlist, name='show_wishlist'),
    path('status_favorite_product/', status_favorite_product ,name='status_favorite_product'),

]

# _________________________________________________________________