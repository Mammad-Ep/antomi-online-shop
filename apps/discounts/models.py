from django.db import models
from my_modules import MaxValueValidator,MinValueValidator
from my_modules import datetime
from apps.products.models import Product
# _________________________________________________________________

class DiscountCoupon(models.Model):
    coupon_title = models.CharField(max_length=50,verbose_name='عنوان کوپن')
    is_active = models.BooleanField(default=False,verbose_name='فعال/غیرفعال')
    discount = models.IntegerField(default=0,
                                           validators=[MinValueValidator(0),MaxValueValidator(100)],
                                           verbose_name='تخفیف')
    start_date = models.DateTimeField(verbose_name='تاریخ شروع')
    end_date = models.DateTimeField(verbose_name='تاریخ پایان')
    
    def __str__(self):
        return self.coupon_title
    
    class Meta:
        verbose_name = 'کوپن تخفیف'
        verbose_name_plural = 'کوپن های تخفیف'
# _________________________________________________________________

class DiscountBasket(models.Model):
    discount_basket_title = models.CharField(max_length=200,verbose_name='عنوان سبد تخفیف')
    is_active = models.BooleanField(default=False,verbose_name='فعال/غیرفعال')
    discount = models.IntegerField(default=0,
                                           validators=[MinValueValidator(0),MaxValueValidator(100)],
                                           verbose_name='تخفیف')
    start_date = models.DateTimeField(verbose_name='تاریخ شروع')
    end_date = models.DateTimeField(verbose_name='تاریخ پایان')
    
    def __str__(self):
        return self.discount_basket_title
    
    class Meta:
        verbose_name = 'سبد تخفیف'
        verbose_name_plural = 'سبدهای تخفیف'
# _________________________________________________________________

class DiscountBasketDetails(models.Model):
    product = models.ForeignKey(Product, verbose_name='محصول', on_delete=models.CASCADE,related_name='product_discounts')
    discount_basket = models.ForeignKey(DiscountBasket, verbose_name='سبد تخفیف', on_delete=models.CASCADE,related_name='discount_basket_details')
    
    class Meta:
        verbose_name = 'جزئیات سبد تخفیف'
        verbose_name_plural = 'جزئیات سبد تخفیف ها'
# _________________________________________________________________
