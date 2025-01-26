from django.db import models
from apps.accounts.models import CustomUser
from apps.products.models import Product
# _________________________________________________________________

class Favorites(models.Model):
    favorite_user = models.ForeignKey(CustomUser, verbose_name='کاربرعلاقه مند', on_delete=models.CASCADE,related_name='user_favorites')
    product = models.ForeignKey(Product, verbose_name='محصول', on_delete=models.CASCADE,related_name='product_favorites')
    register_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    
    def __str__(self):
        return f'{self.favorite_user.name} - {self.product.product_name}'
    
    class Meta:
        verbose_name = 'محصول موردعلاقه'
        verbose_name_plural = 'محصولات موردعلاقه'
# _________________________________________________________________