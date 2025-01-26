from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
import utils
# _________________________________________________________________

class CustomUserManager(BaseUserManager):
    def create_user(self,mobile_number,name="",family="",email="",gender=None,active_code=None,password=None):
        if not mobile_number:
            ValueError('موبایل نباید خالی باشد')
        
        user = self.model(
            mobile_number = mobile_number,
            name = name,
            family = family,
            email = self.normalize_email(email),
            gender = gender,
            active_code = active_code,
        )
        
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self,mobile_number,name,family,email,gender=None,active_code=None,password=None):
        user = self.create_user(
            mobile_number = mobile_number,
            name=name,
            family=family,
            email=email,
            gender=gender,
            active_code=active_code,
        )
        
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        
        return user
        
# _________________________________________________________________

class CustomUser(AbstractBaseUser,PermissionsMixin):
    mobile_number = models.CharField(max_length=11,unique=True,verbose_name='شماره موبایل')
    name = models.CharField(max_length=30,null=True,verbose_name='نام')
    family = models.CharField(max_length=50,null=True,verbose_name='نام خانوادگی')
    email = models.EmailField(max_length=254,null=True,blank=True,verbose_name='ایمیل')
    GENDER_CHOICES = [
        ('man','مرد'),
        ('female','زن'),
    ]
    
    gender = models.CharField(max_length=50,choices=GENDER_CHOICES,default='man',null=True,blank=True,verbose_name='جنسیت')
    is_active = models.BooleanField(default=False,verbose_name='فعال/غیرفعال')
    is_admin = models.BooleanField(default=False,verbose_name='کاربر ادمین/معمولی')
    active_code = models.CharField(max_length=7,null=True,blank=True,verbose_name='کد تایید')
    register_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    update_date = models.DateTimeField(auto_now=True,verbose_name='تاریخ ویرایش')

    def __str__(self):
        return f'{self.name} {self.family} : {self.mobile_number}'
        
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = "mobile_number"
    REQUIRED_FIELDS = ["name","family","email"]
    
    
    @property
    def is_staff(self):
        return self.is_admin
    
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
# _________________________________________________________________

class Customer(models.Model):
    user = models.OneToOneField(CustomUser, verbose_name='کاربر/مشتری', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11,null=True,verbose_name='تلفن ثابت')
    postal_code = models.CharField(max_length=10,null=True,verbose_name='کدپستی')
    address = models.CharField(max_length=500,null=True,verbose_name='آدرس')
    file_upload = utils.FileUpload('accounts_app','customer')
    image_name = models.ImageField(upload_to=file_upload.upload_to,null=True,blank=True,verbose_name='عکس پروفایل')
    register_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    update_date = models.DateTimeField(auto_now=True,verbose_name='تاریخ ویرایش')
    
    def __str__(self):
        return self.user.name+ " "+self.user.family
    
    class Meta:
        verbose_name = 'مشتری'
        verbose_name_plural = 'مشتری ها'
# _________________________________________________________________