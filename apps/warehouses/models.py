from django.db import models
from apps.accounts.models import CustomUser
from apps.products.models import Product
# _________________________________________________________________

class PurchaseWarehouse(models.Model):
    user_registred = models.ForeignKey(CustomUser, verbose_name='کاربر', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='محصول', on_delete=models.CASCADE,related_name='product_purchases')
    purchase_price = models.IntegerField(verbose_name='قیمت خرید')
    qty = models.PositiveIntegerField(verbose_name='تعداد')
    register_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    update_date = models.DateTimeField(auto_now=True,verbose_name='تاریخ ویرایش')
    
    def __str__(self):
        return f'{self.product.product_name}'
    
    
    class Meta:
        verbose_name = 'انبار خرید محصول'
        verbose_name_plural = 'انبار خرید محصولات'
# _________________________________________________________________

class SalesWarehouse(models.Model):
    user_registred = models.ForeignKey(CustomUser, verbose_name='کاربر', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='محصول', on_delete=models.CASCADE,related_name='product_sales')
    sale_price = models.IntegerField(verbose_name='قیمت فروش')
    qty = models.PositiveIntegerField(verbose_name='تعداد')
    register_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    update_date = models.DateTimeField(auto_now=True,verbose_name='تاریخ ویرایش')
    
    def __str__(self):
        return f'{self.product.product_name}'
    
    class Meta:
        verbose_name = 'انبار فروش محصول'
        verbose_name_plural = 'انبار فروش محصولات'
# _________________________________________________________________