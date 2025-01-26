from django.urls import path
from .views import *
# _________________________________________________________________

app_name = 'products'

urlpatterns = [
    path('ajax_admin/', get_filter_value_for_feature ,name='filter_value_for_feature'),
    path('Popular_product_categories/', popular_product_categories ,name='Popular_product_categories'),
    path('latest_products/', latest_products ,name='latest_products'),
    path('best_selling_products/', best_selling_products ,name='best_selling_products'),
    path('cheapest_products/', cheapest_products ,name='cheapest_products'),
    path('product/<slug:slug>', ProductView.as_view() ,name='product'),
    path('related_products/<slug:slug>', related_products ,name='related_products'),
    path('related_best_selling_products/<slug:slug>', related_best_selling_products ,name='related_best_selling_products'),
    
    path('productslist/<slug:slug>', ProductsList.as_view() ,name='productslist'),
    path('product_category_productsList/<slug:slug>', product_category_productsList ,name='product_category_productsList'),
    path('brand_filter_productsList/<slug:slug>', brand_filter_productsList ,name='brand_filter_productsList'),
    path('feature_filter_productsList/<slug:slug>', feature_filter_productsList ,name='feature_filter_productsList'),
    
    path('compare_products/', CompareProductView.as_view() ,name='compare_products'),
    path('compare_produts_list/', compare_produts_list ,name='compare_produts_list'),
    path('add_compare_product/', add_compare_product ,name='add_compare_product'),
    path('remove_compare_product/', remove_compare_product ,name='remove_compare_product'),
    path('status_compare_product/', status_compare_product ,name='status_compare_product'),

]

# _________________________________________________________________
