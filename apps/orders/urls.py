from django.urls import path
from .views import *
# _________________________________________________________________

app_name = 'orders'

urlpatterns = [
    path('cart/', ShopCartView.as_view() ,name='cart'),
    path('show_shop_cart/', show_shop_cart ,name='show_shop_cart'),
    path('add_shop_cart/', add_shop_cart ,name='add_shop_cart'),
    path('update_shop_cart/', update_shop_cart ,name='update_shop_cart'),
    path('remove_shop_cart/', remove_shop_cart ,name='remove_shop_cart'),
    path('status_shop_cart/', status_shop_cart ,name='status_shop_cart'),
    path('applay_coupon_cart/', applay_coupon_cart ,name='applay_coupon_cart'),
    path('create_order/', create_order ,name='create_order'),
    path('checkout_cart/<slug:slug>', CheckoutCart.as_view() ,name='checkout_cart'),

]
# _________________________________________________________________
