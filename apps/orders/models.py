from django.db import models
from apps.accounts.models import Customer
from apps.products.models import Product
from my_modules import uuid
from my_modules import MaxValueValidator
from my_modules import MinValueValidator
import utils
# _________________________________________________________________

class PaymentType(models.Model):
    payment_type_title = models.CharField(max_length=50,verbose_name='نوع پرداخت')
    
    def __str__(self):
        return self.payment_type_title
    
    class Meta:
        verbose_name = 'نوع پرداخت'
        verbose_name_plural = 'انواع روش پرداخت'

# _________________________________________________________________

class OrderState(models.Model):
    order_state_title = models.CharField(max_length=50,verbose_name='وضعیت سفارش')
    
    def __str__(self):
        return self.order_state_title
    
    class Meta:
        verbose_name = 'وضعیت سفارش'
        verbose_name_plural = 'وضعیت های سفارش'

# _________________________________________________________________

class Order(models.Model):
    customer = models.ForeignKey(Customer, verbose_name='مشتری/کاربر', on_delete=models.CASCADE,related_name='customer_orders')
    is_finaly = models.BooleanField(default=False, verbose_name='نهایی شده')
    description = models.TextField(verbose_name='توضیحات سفارش',null=True,blank=True)
    order_code_sample = 'antomi'+str(utils.get_random_code(7))
    order_code = models.CharField(max_length=50,default=order_code_sample,unique=True,verbose_name='کد سفارش')
    slug = models.SlugField(default=uuid.uuid4,unique=True)
    register_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    update_date = models.DateTimeField(auto_now=True,verbose_name='تاریخ ویرایش')
    invoice_amount = models.IntegerField(default=0, verbose_name='مبلغ فاکتور')
    discount = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(100)])
    order_state = models.ForeignKey(OrderState, verbose_name='وضعیت سفارش', on_delete=models.CASCADE,null=True,blank=True)
    payment_type = models.ForeignKey(PaymentType, verbose_name='روش پرداخت', on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return self.order_code
    
    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'


# _________________________________________________________________

class orderDetails(models.Model):
    product = models.ForeignKey(Product, verbose_name='محصول', on_delete=models.CASCADE,related_name='product_order_details')
    order = models.ForeignKey(Order, verbose_name='سفارش', on_delete=models.CASCADE,related_name='order_details')
    price = models.IntegerField(verbose_name='قیمت')
    qty = models.IntegerField(verbose_name='تعداد',default=1)
    register_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')

    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name = 'جزئیات سفارش'
        verbose_name_plural = 'جزئیات سفارش ها'
# _________________________________________________________________
