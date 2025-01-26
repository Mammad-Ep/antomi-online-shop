from django.shortcuts import render,redirect
from my_modules import JsonResponse
from my_modules import Max
from my_modules import Min
from my_modules import Count
from my_modules import Sum
from my_modules import Avg
from my_modules import Q
from my_modules import View
from my_modules import get_object_or_404
from my_modules import HttpResponse
from my_modules import Paginator
from .filters import FilterPrice
from .compare import CompareProduct
from .models import (FeatureValue,Product,ProuctGroup,Brand,FeatureType)
# _________________________________________________________________

# two dropdown in adminpanel
# فیلتر مقادیر ویژگی برای ویژگی در پنل ادمین

def get_filter_value_for_feature(request):
    if request.method == 'GET':
        feature_id=request.GET['feature_id']
        feature_values=FeatureValue.objects.filter(feature_id=feature_id)
        res={fv.value_name:fv.id for fv in feature_values}
        
        return JsonResponse(data=res , safe=False)

# _________________________________________________________________

def popular_product_categories(request):
    products_groups = ProuctGroup.objects.filter(Q(is_active=True) & ~Q(group_parent=None))\
    .annotate(count_products=Count('products_groups'))\
        .filter(~Q(count_products=0))\
            .order_by('-count_products')
    
    return render(request,'products_app/partials/popular_categories.html',{'products_groups':products_groups})

# _________________________________________________________________

def  latest_products(request):

    products_groups={}
    groups = ProuctGroup.objects.filter(Q(is_active=True) & Q(general_group=True))\
        .annotate(count_products=Count('products_groups'))\
            .order_by('-count_products')[:4]
    
    for group in groups:
        products_groups[group]=group.products_groups.filter(Q(is_active=True)).order_by('-published_date')[:6]        
    
    
    return render(request,'products_app/partials/latest_products.html',{'products_groups':products_groups})
# _________________________________________________________________

def best_selling_products(request):
    products_groups={}
    groups = ProuctGroup.objects.filter(Q(is_active=True) & Q(general_group=True))\
        .annotate(count_products=Count('products_groups'))\
            .order_by('-count_products')[:4]
    
    for group in groups:
        products_groups[group]=group.products_groups.filter(Q(is_active=True))\
        .annotate(number_sales=Sum('product_sales__qty'))\
        .order_by('-number_sales')[:6]
        
    return render(request,'products_app/partials/best_selling_products.html',{'products_groups':products_groups})
# _________________________________________________________________

def cheapest_products(request):
    products_groups={}
    groups = ProuctGroup.objects.filter(Q(is_active=True) & Q(general_group=True))\
        .annotate(count_products=Count('products_groups'))\
            .order_by('-count_products')[:4]
    
    for group in groups:
        products_groups[group]=group.products_groups.filter(Q(is_active=True)).order_by('product_price')[:6]
        
    return render(request,'products_app/partials/cheapest_products.html',{'products_groups':products_groups})
# _________________________________________________________________

class ProductView(View):
    template_name = 'products_app/product.html'
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product,slug=kwargs['slug'])
        general_group = product.product_group.filter(general_group=True)[0]
        feature_types = []
        
        for item in product.product_features.all():
            if item.feature_type not in feature_types:
                feature_types.append(item.feature_type)
                
        if product.is_active:
            context ={
                'product':product,
                'general_group':general_group,
                'feature_types':feature_types
            }
            return render(request,self.template_name,context)
# _________________________________________________________________

def related_products(request,slug):
    current_product = get_object_or_404(Product,slug=slug)
    main_group = current_product.product_group.all()[0]
    products = Product.objects.filter(Q(is_active=True) & Q(product_group=main_group) & ~Q(id=current_product.id))
    # print(main_group) لپ تاپ
    return render(request,'products_app/partials/related_products.html',{'products':products})
# _________________________________________________________________

def related_best_selling_products(request,slug):
    current_product = get_object_or_404(Product,slug=slug)
    main_group = current_product.product_group.all()[0]
    products = Product.objects.filter(Q(is_active=True) & Q(product_group=main_group) & ~Q(id=current_product.id))\
    .annotate(selling_products=Sum('product_sales__qty')).order_by('-selling_products')[:5]
    
    return render(request,'products_app/partials/related_best_selling_products.html',{'products':products})
# _________________________________________________________________

class ProductsList(View):
    template_name = 'products_app/products_list.html'
    def get(self, request, *args, **kwargs):
        
        group = get_object_or_404(ProuctGroup,slug=kwargs['slug'])
        products = group.products_groups.all()
        
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
        
        
        # Paginator
        paginator = Paginator(products,8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context ={
            'products':products,
            'group':group,
            'price_aggregate':price_aggregate,
            'select_sort':select_sort,
            'page_obj':page_obj,
            'price_max':price_max,
            'price_min':price_min,
            
        }
        return render(request,self.template_name,context)
# _________________________________________________________________

def product_category_productsList(request,slug):
    
    product_group = get_object_or_404(ProuctGroup,slug=slug)
    
    groups = product_group.groups.filter(is_active=True)\
    .annotate(count_products=Count('products_groups'))\
        .filter(~Q(count_products=0)).order_by('-count_products')
    
    return render(request,'products_app/partials/product_category_productsList.html',{'groups':groups})
# _________________________________________________________________

def brand_filter_productsList(request,slug):
    product_group = get_object_or_404(ProuctGroup,slug=slug)
    brand_id_list = product_group.products_groups.values('brand_id')
    brands = Brand.objects.filter(id__in=brand_id_list)\
        .annotate(count_products=Count('brand_products'))\
            .filter(~Q(count_products=0)).order_by('-count_products')
            
    return render(request,'products_app/partials/brand_filter_productsList.html',{'brands':brands})
# _________________________________________________________________

def feature_filter_productsList(request,slug):
    product_group = get_object_or_404(ProuctGroup,slug=slug)
    features = product_group.groups_features.all()
    feature_values = dict()
    for feature in features:
        if feature.feature_for_filter==True:
            feature_values[feature]=feature.feature_values.all()
        
    return render(request,'products_app/partials/feature_filter_productsList.html',{'feature_values':feature_values})

# =================================================================

## Compare Products

class CompareProductView(View):
    template_name = 'products_app/compare_products.html'
    def get(self, request, *args, **kwargs):
        
        return render(request,self.template_name)
# _________________________________________________________________

def compare_produts_list(request):
    compare = CompareProduct(request) 
    product_id_list = compare.compare_product
    products = Product.objects.filter(id__in = product_id_list)
    
    features = []
    
    for product in products:
        for item in product.product_features.all():
            if not item.feature in features and item.feature.feature_for_filter == True:
                features.append(item.feature)
    
    context = {
        'products':products,
        'features':features
    }
    return render(request,'products_app/partials/compare_products_list.html',context)
# _________________________________________________________________

def status_compare_product(request):
    compare = CompareProduct(request) 
    return HttpResponse(compare.count)
# _________________________________________________________________

def add_compare_product(request):
    product_id = request.GET.get('product_id')
    group_id = request.GET.get('group_id')
    message = 'محصول اضافه نشد'
    compare = CompareProduct(request)   
    temp1 = compare.count
    compare.add_compare_product(product_id,group_id)
    temp2 = compare.count
    
    if temp2 > temp1:
        message = f'محصول اضافه شد: ({temp2} محصول)'
        
    return HttpResponse(message)
    
# _________________________________________________________________

def remove_compare_product(request):
    product_id = request.GET.get('product_id')
    group_id = request.GET.get('group_id')
    compare = CompareProduct(request)
    compare.remove_compare_product(product_id,group_id)
    
    return redirect('products:compare_produts_list')
# _________________________________________________________________

