from django.db import models
from apps.accounts.models import CustomUser
from apps.products.models import Product
from my_modules import MaxValueValidator,MinValueValidator
# _________________________________________________________________

class Scoring(models.Model):
    scoring_user = models.ForeignKey(CustomUser, verbose_name='کاربر/مشتری', on_delete=models.CASCADE,related_name='user_scores')
    product = models.ForeignKey(Product, verbose_name='محصول', on_delete=models.CASCADE,related_name='product_scores')
    score = models.PositiveIntegerField(verbose_name='امتیاز',validators=[MinValueValidator(1),MaxValueValidator(5)])
    register_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    
    def __str__(self):
        return self.score
    
    class Meta:
        verbose_name = 'امتیاز محصول'
        verbose_name_plural = 'امتیازات محصولات'
# _________________________________________________________________
