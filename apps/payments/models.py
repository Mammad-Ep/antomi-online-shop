from django.db import models
from apps.accounts.models import Customer
from apps.orders.models import Order
# _________________________________________________________________

class Payment(models.Model):
    customer = models.ForeignKey(Customer, verbose_name='مشتری/کاربر', on_delete=models.CASCADE,related_name='customer_payments')
    order = models.ForeignKey(Order, verbose_name='سفارش', on_delete=models.CASCADE, related_name='order_payments')
    is_finaly = models.BooleanField(default=False, verbose_name='نهایی شده')
    ref_id = models.CharField(max_length=50, verbose_name='کدپیگیری',null=True,blank=True)
    status_code = models.CharField(max_length=50, verbose_name='کد وضعیت',null=True,blank=True)
    invoice_amount = models.IntegerField(verbose_name='مبلغ فاکتور',default=0)
    register_date = models.DateTimeField(verbose_name='تاریخ درج', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)
    description = models.TextField(verbose_name='توضیحات پرداخت',null=True,blank=True)
    
    def __str__(self):
        return self.ref_id
    
    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت ها'
    
# _________________________________________________________________