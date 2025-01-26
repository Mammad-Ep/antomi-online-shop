from django.shortcuts import render,redirect
from apps.products.models import ProuctGroup
from apps.products.models import Product
from my_modules import View
from my_modules import Count
from my_modules import Q
from my_modules import Min
from my_modules import Max
from my_modules import Avg
from my_modules import Sum
from my_modules import Paginator
from my_modules import get_object_or_404
# _________________________________________________________________

def search_box_area(request):
    general_groups = ProuctGroup.objects.filter(is_active=True,general_group=True)\
        .annotate(count_products=Count('products_groups'))\
            .filter(~Q(count_products=0))\
                .order_by('-count_products')
    return render(request,'search_app/search_box_area.html',{'general_groups':general_groups})
# _________________________________________________________________

class SearchView(View):
    template_name = 'search_app/search_result.html'
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        group_search = request.GET.get('group-search')
        if group_search == 'all-categori':
            products = Product.objects.filter(Q(product_name__icontains=q)| Q(brand__brand_name__icontains=q))
            return render(request,'search_app/search_without_categori.html',{'products':products})
        
        group = get_object_or_404(ProuctGroup,group_name=group_search)
        products = group.products_groups.filter(product_name__icontains=q,brand__brand_name__icontains=q)
        
        
        price_aggregate = products.aggregate(min_price=Min('product_price'),
                                             max_price=Max('product_price'),
                                             avg_price=Avg('product_price'),)   
        
        # filter-feature
        feature_filter = request.GET.getlist('feature')
        if feature_filter:
            products = products.filter(product_features__filter_value_id__in=feature_filter).distinct()
        
        # filter-brand    
        brand_filter = request.GET.getlist('brand')
        if brand_filter:
            products = products.filter(brand_id__in=brand_filter)
                

        # filter-price
        price_min = 0
        price_max = 0
        if 'price_min' in request.GET:
            price_min = request.GET.get('price_min')
            price_max = request.GET.get('price_max')
            
            products = products.filter(product_price__range=(price_min,price_max))
        # price_filter = FilterPrice(request.GET,queryset=products)

 
        # Select-sort
        select_sort = request.GET.get('sort_type')
        
        if not select_sort or select_sort == 'best-selling':            
            products = products.annotate(count_sales=Sum('product_sales__qty')).order_by('-count_sales')
            
        if select_sort == 'upward-price':
            products = products.order_by('-product_price')
        
        if select_sort == 'downward-price':
            products = products.order_by('product_price')
        
        if select_sort == 'highest-score':
            products = products.annotate(count_score=Avg('product_scores__score')).order_by('-count_score')        
        
        
        context ={
            'products':products,
            'group':group,
            'price_aggregate':price_aggregate,
            'select_sort':select_sort,
            'price_max':price_max,
            'price_min':price_min,
            
        }
        
        return render(request,self.template_name,context)
# _________________________________________________________________
