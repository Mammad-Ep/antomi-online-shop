
import django_filters

class FilterPrice(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name='product_price',lookup_expr='lte')
    price_max = django_filters.NumberFilter(field_name='product_price',lookup_expr='gte')