from django.db import models
from apps.accounts.models import CustomUser
from apps.products.models import Product
from middlewares.middlewares import RequestMiddleware
from my_modules import Sum
# _________________________________________________________________

class CommentProduct(models.Model):
    user_commenter = models.ForeignKey(CustomUser, verbose_name='کاربرنظرهنده', on_delete=models.CASCADE,related_name='user_comments')
    product = models.ForeignKey(Product, verbose_name='محصول', on_delete=models.CASCADE,related_name='product_comments')
    is_active = models.BooleanField(default=False,verbose_name='فعال/غیرفعال')
    user_confirming = models.ForeignKey(CustomUser, verbose_name='کاربر تاییدکننده',null=True,blank=True, on_delete=models.CASCADE)
    register_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    update_date = models.DateTimeField(auto_now=True,verbose_name='تاریخ ویرایش')
    fullname = models.CharField(max_length=50,verbose_name='نام کامل')
    email = models.EmailField(max_length=254,verbose_name='ایمیل',null=True,blank=True)
    comment_text = models.TextField(verbose_name='متن نظر')
    comment_parent = models.ForeignKey("CommentProduct", verbose_name='والد نظر', on_delete=models.CASCADE,null=True,blank=True,related_name='commnets_child')
    
    # ---------------------------------------
    def check_like_comment(self):
        request=RequestMiddleware(get_response=None)
        request=request.thread_local.current_request
        
        flag = self.comment_likes.filter(user_like=request.user).exists()
        
        return flag    
    # ---------------------------------------
    def get_number_like_dislike(self):
        like = self.comment_likes.filter(like_type_id=1).aggregate(Sum('like_number'))['like_number__sum']
        dislike = self.comment_likes.filter(like_type_id=2).aggregate(Sum('like_number'))['like_number__sum']
        
        like_number = 0
        dislike_number = 0
        
        if like != None:
            like_number = like
            
        if dislike != None:
            dislike_number = dislike
            
        return like_number,dislike_number
    # ---------------------------------------
    
    def __str__(self):
        return self.fullname
    
    class Meta:
        verbose_name = 'نظرمحصول'
        verbose_name_plural = 'نظرات محصولات'
# _________________________________________________________________

class CommentLikeType(models.Model):
    like_type = models.CharField(max_length=20,verbose_name='نوع لایک')

    def __str__(self):
        return self.like_type
    
    class Meta:
        verbose_name = 'نوع لایک'
        verbose_name_plural = 'انواع لایک ها'
# _________________________________________________________________

class CommentLike(models.Model):
    comment = models.ForeignKey(CommentProduct, verbose_name='کامنت', on_delete=models.CASCADE,related_name='comment_likes')
    user_like = models.ForeignKey(CustomUser, verbose_name='کاربر', on_delete=models.CASCADE)
    like_number = models.PositiveIntegerField(default=0,verbose_name='تعداد لایک')
    register_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    
    like_type = models.ForeignKey(CommentLikeType,null=True,blank=True,verbose_name='نوع لایک', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.like_number
    
    
    class Meta:
        verbose_name = 'لایک کامنت'
        verbose_name_plural = 'لایک های کامنت'
# _________________________________________________________________
