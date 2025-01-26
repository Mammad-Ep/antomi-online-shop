from django.db import models
import utils
from datetime import datetime
from my_modules import RichTextUploadingField
from my_modules import uuid
from my_modules import os
from my_modules import Q
from my_modules import Min
from my_modules import Max
from my_modules import Count
from my_modules import Avg
from my_modules import Sum
from my_modules import mark_safe
from my_modules import reverse
from middlewares.middlewares import RequestMiddleware
# _________________________________________________________________

class Brand(models.Model):
    brand_name = models.CharField(max_length=100,verbose_name='نام برند')
    register_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    file_upload = utils.FileUpload('products_app','brand')
    image_name = models.ImageField(upload_to=file_upload.upload_to,verbose_name='عکس برند')
    slug = models.SlugField(null=True,blank=True)
    
    def __str__(self):
        return self.brand_name

    
    def image(self):
        return mark_safe(f'<img src="/media/{self.image_name}/" style="height:70px; width:70px>')   
    image.short_description = 'عکس برند'
    
    class Meta:
        verbose_name = 'ّبرند'
        verbose_name_plural = 'برندها'


# _________________________________________________________________

class ProuctGroup(models.Model):
    group_name = models.CharField(max_length=200,verbose_name='نام گروه محصول')
    description = models.TextField(null=True,blank=True,verbose_name='توضیحات')
    is_active = models.BooleanField(default=False,verbose_name='فعال/غیرفعال')
    slug = models.SlugField(null=True,blank=True)
    file_upload = utils.FileUpload('products_app','productGroup')
    image_name = models.ImageField(upload_to=file_upload.upload_to,verbose_name='عکس گروه محصول')
    register_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    update_date = models.DateTimeField(auto_now=True,verbose_name='تاریخ ویرایش')
    published_date = models.DateTimeField(default=datetime.now(),verbose_name='تاریخ انتشار')
    general_group = models.BooleanField(default=False,verbose_name='گروه عمومی')
    
    group_parent = models.ForeignKey("ProuctGroup", verbose_name='والد گروه', null=True,blank=True, on_delete=models.CASCADE,related_name='groups')
    
    def __str__(self):
        return self.group_name
    
    class Meta:
        verbose_name = 'گروه محصول'
        verbose_name_plural = 'گروه های محصولات'
# _________________________________________________________________

class Feature(models.Model):
    feature_name = models.CharField(max_length=50,verbose_name='نام ویژگی')
    product_group = models.ManyToManyField(ProuctGroup, verbose_name='گروه محصول',related_name='groups_features')
    feature_for_filter = models.BooleanField(default=False,verbose_name='ویژگی برای فیلتر محصولات')
    
    def __str__(self):
        return self.feature_name
    
    class Meta:
        verbose_name = 'ویژگی'
        verbose_name_plural = 'ویژگی ها'
# _________________________________________________________________

class FeatureValue(models.Model):
    value_name = models.CharField(max_length=200,verbose_name='مقدار ویژگی')
    feature = models.ForeignKey(Feature, verbose_name='ویژگی', on_delete=models.CASCADE,related_name='feature_values')

    def __str__(self):
        return self.value_name
    
    class Meta:
        verbose_name = 'مقدار ویژگی'
        verbose_name_plural = 'مقادیر ویژگی ها'
# _________________________________________________________________

class Product(models.Model):
    product_name = models.CharField(max_length=300,verbose_name='نام محصول')
    summery_description = models.TextField(null=True,blank=True,verbose_name='توضیحات خلاصه')
    description = RichTextUploadingField(null=True,blank=True,verbose_name='توضیحات')
    product_price = models.IntegerField(verbose_name='قیمت محصول')
    is_active = models.BooleanField(default=False,verbose_name='فعال/غیرفعال')
    slug = models.SlugField(null=True,blank=True)
    file_upload = utils.FileUpload('products_app','product')
    image_name = models.ImageField(upload_to=file_upload.upload_to,verbose_name='عکس محصول')
    register_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    update_date = models.DateTimeField(auto_now=True,verbose_name='تاریخ ویرایش')
    published_date = models.DateTimeField(default=datetime.now(),verbose_name='تاریخ انتشار')
    
    brand = models.ForeignKey(Brand, verbose_name='برند', on_delete=models.CASCADE,related_name='brand_products')
    product_group = models.ManyToManyField(ProuctGroup, verbose_name='گروه محصول',related_name='products_groups')
    feature = models.ManyToManyField(Feature, verbose_name='ویژگی',through='ProductFeature')
    # -------------------------------------
    
    def __str__(self):
        return self.product_name
    # -------------------------------------
    
    def product_image(self):
        return mark_safe(f'<img src="/media/{self.image_name}/" style="height:100px; width:150px;>')   
    product_image.short_description = 'عکس برند'
    # -------------------------------------
    
    def get_absolute_url(self):
        return reverse("products:product",kwargs={"slug":self.slug})
        
    # -------------------------------------
    
    def get_main_group(self):
        return self.product_group.all()[0].id
        
    # -------------------------------------
    
    def price_by_discount(self):
        discount_filter=self.product_discounts.filter(
            Q(discount_basket__is_active=True)&
                Q(discount_basket__start_date__lte=datetime.now())&
                Q(discount_basket__end_date__gte=datetime.now())
        ).aggregate(Max('discount_basket__discount'))
        
        discount=0

        if discount_filter['discount_basket__discount__max']!=None:
            discount = discount_filter['discount_basket__discount__max']
        
            
        return self.product_price - (self.product_price * (discount/100))
    
    # -------------------------------------
    
    def number_product_warehouse(self):
        number_purchase = self.product_purchases.aggregate(Sum('qty'))
        number_sales = self.product_sales.aggregate(Sum('qty'))
    
        input=0
        if number_purchase['qty__sum']!=None:
            input = number_purchase['qty__sum']
           
        output=0 
        if number_sales['qty__sum']!=None:
            output = number_sales['qty__sum']
            
        return input - output
    number_product_warehouse.short_description = 'تعداد موجودی'
    
    # -------------------------------------
    
    def avg_score_product(self):
        score = 0
        score_avg = self.product_scores.aggregate(Avg('score'))['score__avg']
        
        if score_avg!=None:
            score = score_avg
        
        return score
    
    # -------------------------------------
    
    def user_score_product(self):
        request=RequestMiddleware(get_response=None)
        request=request.thread_local.current_request
        
        user_score = self.product_scores.filter(scoring_user=request.user)
        
        score = 0
        if user_score:
            score = user_score[0].score
            
        return score
    
    # -------------------------------------
    
    def check_favorite_product(self):
        request=RequestMiddleware(get_response=None)
        request=request.thread_local.current_request
        
        flag = self.product_favorites.filter(favorite_user=request.user).exists()
        
        return flag
    # -------------------------------------
    
    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
# _________________________________________________________________

class FeatureType(models.Model):
    feature_type = models.CharField(max_length=100,verbose_name='نوع ویژگی')
    
    def __str__(self):
        return self.feature_type
    
    class Meta:
        verbose_name = 'نوع ویژگی'
        verbose_name_plural = 'نوع های ویژگی'
# _________________________________________________________________

class ProductFeature(models.Model):
    feature_value = models.CharField(max_length=100,verbose_name='مقدار ویژگی')
    product = models.ForeignKey(Product, verbose_name='محصول', on_delete=models.CASCADE,related_name='product_features')
    feature = models.ForeignKey(Feature, verbose_name='ویژگی', on_delete=models.CASCADE)
    filter_value = models.ForeignKey(FeatureValue, verbose_name='مقدار ویژگی', on_delete=models.CASCADE)
    feature_type = models.ForeignKey(FeatureType, verbose_name='نوع ویژگی', null=True,blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.feature_value
    
    class Meta:
        verbose_name = 'ویژگی محصول'
        verbose_name_plural = 'ویژگی های محصولات'
# _________________________________________________________________

def upload_to(instance,filename):
    file,exe = os.path.splitext(filename)
    return f'images/products_app/product_gallery/{instance.product.id}/{file}{uuid.uuid4}{exe}'

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, verbose_name='محصول', on_delete=models.CASCADE,related_name='product_images')    
    image_name = models.ImageField(upload_to=upload_to,verbose_name='عکس محصول')
    register_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')

    def __str__(self):
        return self.id
    
    class Meta:
        verbose_name = 'عکس محصول'
        verbose_name_plural = 'عکس های محصولات'
            
# _________________________________________________________________

