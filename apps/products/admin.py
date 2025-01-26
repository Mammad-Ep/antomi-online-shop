from django.contrib import admin
from my_modules import mark_safe
from my_modules import short_description
from my_modules import Count
from my_modules import Q
from my_modules import HttpResponse
from my_modules import serializers
from my_modules import DropdownFilter
from .models import (Brand,ProuctGroup,Feature,FeatureType,
                     FeatureValue,Product,ProductFeature,ProductGallery)
# _________________________________________________________________

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name','register_date','slug','count_products',) #'image'
    list_filter = ('brand_name',)
    ordering = ('register_date',)
    search_fields = ('brand_name',)

    def get_queryset(self, *args, **kwargs):
        queryset = super(BrandAdmin, self).get_queryset(*args, **kwargs)
        queryset = queryset.annotate(products_count=Count('brand_products'))
        return queryset
    
    @short_description('تعداد محصولات برند')
    def count_products(self,obj):
        return obj.products_count
# _________________________________________________________________

@short_description('غیرفعال کردن آیتم های انتخاب شده')
def de_active_items(modeldmin,request,queryset):
    res = queryset.update(is_active=False)
    message = f'تعداد {res} آیتم غیرفعال شد.'
    modeldmin.message_user(request,message)

@short_description('فعال کردن آیتم های انتخاب شده')
def active_items(modeldmin,request,queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} آیتم فعال شد.'
    modeldmin.message_user(request,message)

@short_description('گرفتن خروجی جیسون از موارد انتخاب شده')
def export_json(modeldmin,request,queryset):
    response = HttpResponse(content_type='application/json')
    serializers.serialize('json',queryset,stream=response)
    return response
# _________________________________________________________________

@admin.register(ProuctGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ('group_name','is_active','register_date','general_group','published_date','features_of_groups','count_products')
    list_filter = ('group_name','is_active',)
    search_fields = ('group_name',)
    list_editable = ('is_active',)
    ordering = ('register_date',)
    actions = (de_active_items,active_items,export_json)

    @short_description('ویژگی های گروه')
    def features_of_groups(self,obj):
        return ' , '.join([item.feature_name for item in obj.groups_features.all()])
    
    
    def get_queryset(self, *args, **kwargs):
        queryset = super(ProductGroupAdmin, self).get_queryset(*args, **kwargs)
        queryset = queryset.annotate(products_count=Count('products_groups'))
        return queryset
    
    @short_description('تعداد محصولات گروه')
    def count_products(self,obj):
        return obj.products_count
    
    
# _________________________________________________________________

@admin.register(FeatureType)
class FeatureTypeAdmin(admin.ModelAdmin):
    list_display = ('id','feature_type')
    search_fields = ('feature_type',)
    list_filter = ('feature_type',)
    ordering = ('feature_type',)
# _________________________________________________________________

class FeatureValueInline(admin.TabularInline):
    model = FeatureValue
    extra = 3

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('feature_name','feature_groups','feature_values')
    list_filter = ('feature_name',)
    search_fields = ('feature_name',)
    ordering = ('feature_name',)
    inlines = (FeatureValueInline,)
    
    @short_description('گروه های ویژگی')
    def feature_groups(self,obj):
        return ' , '.join([item.group_name for item in obj.product_group.all()])
    
    @short_description('مقدار های ویژگی')
    def feature_values(self,obj):
        return ' , '.join([item.value_name for item in obj.feature_values.all()])
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'product_group':
            kwargs['queryset']=ProuctGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)
# _________________________________________________________________

class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 23
    
    class Media:
        # css={'all':('css/admin_style.css',)}
        
        js=('https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',
            'js/admin_script.js')
    
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 3

@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ('product_name','product_price','is_active','register_date',
                    'update_date','published_date','brand',
                    'product_groups','product_image','features_count','number_product_warehouse')
    
    search_fields = ('product_name','product_price',)
    ordering = ('-register_date','update_date',)
    list_filter = (('product_name',DropdownFilter),'product_price')
    list_editable = ('is_active',)
    inlines = (ProductFeatureInline,ProductGalleryInline)
    actions = (active_items,de_active_items)
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'product_group':
            kwargs['queryset']=ProuctGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
    def get_queryset(self, *args, **kwargs):
        queryset = super(Product, self).get_queryset(*args, **kwargs)
        queryset = queryset.annotate(features_count=Count('product_features'))
        return queryset
    
    @short_description('تعداد ویژگی های محصول')
    def features_count(self,obj):
        return obj.features_count
    
    @short_description('گروه های محصول')
    def product_groups(self,obj):
        return ' , '.join([item.group_name for item in obj.product_group.all()])
    
    
    fieldsets = (
        
        (
            ("اطلاعات محصول"),
         
         {"fields": 
             ("product_name",
             "summery_description",
             "description",
             ("product_price","slug"),
             "product_group",
              "brand",
             "image_name",
             )}
         ),
        
        (
            ("وضعیت محصول"),
            {
                "fields": (
                    "is_active",
                ),
            },
        ),
        (("تاریخ و زمان"), {"fields": ("published_date",)}),
    )
# _________________________________________________________________
