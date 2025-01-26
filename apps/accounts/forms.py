from typing import Any
from my_modules import forms
from my_modules import ReadOnlyPasswordHashField
from my_modules import ValidationError
from my_modules import validators
from .models import CustomUser
import re
# _________________________________________________________________

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(max_length=32, required=True,widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=32, required=True,widget=forms.PasswordInput())
    
    class Meta:
        model= CustomUser
        fields = ['mobile_number','name','family','email']
        
    
    def save(self, commit=True) -> Any:
        user=super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user
# _________________________________________________________________
class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='برای تغییر رمز عبور روی این <a href="../password"> لینک </a> کلیک کنید')
    
    class Meta:
        model = CustomUser
        fields = ['mobile_number','name','family','email']

# _________________________________________________________________

class RegisterUserForm(forms.Form):
    mobile_number = forms.CharField(max_length=11, required=True,
                                    widget=forms.TextInput(attrs={"id":"mobile-register"}),
                                    error_messages={'required':'فیلد موبایل نباید خالی باشد'})
    
    password1 = forms.CharField(max_length=32, required=True,
                                    widget=forms.PasswordInput(attrs={"id":"password1-register"}),
                                    error_messages={'required':'فیلد پسورد نباید خالی باشد'})
    
    password2 = forms.CharField(max_length=32, required=True,
                                    widget=forms.PasswordInput(attrs={"id":"password2-register"}),
                                    error_messages={'required':'فیلد تکرار پسورد نباید خالی باشد'})
    
    def clean_password2(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']
        
        if pass1 and pass2 and pass1!=pass2:
            raise ValidationError('رمزعبور با تکرار آن برابر نمی باشد.')
            
        elif len(pass2) < 8:
            raise ValidationError('رمز عبور نمیتواند کمتر از 8 کاراکتر باشد')
        
        elif not re.findall(r'[0-9]',pass2):
            raise ValidationError('رمز عبور باید عدد داشته باشد')
        
        elif not re.findall(r'[a-z]',pass2):
            raise ValidationError('رمز عبور باید حداقل یک حرف کوچک داشته باشد')
        
        elif not re.findall(r'[A-Z]',pass2):
            raise ValidationError('رمز عبور باید حداقل یک حرف کوچک داشته باشد')
        
        elif not re.findall(r'[@#$%!^&*]',pass2):
            raise ValidationError('رمز عبور باید حداقل یک کاراکتر خاص داشته باشد (@#$%!^&*)')
        
        return pass2
# _________________________________________________________________

from captcha.fields import CaptchaField

class CaptchaTestForm(forms.Form):
    
    captcha_field=CaptchaField()

# _________________________________________________________________

class VerifyUserForm(forms.Form):
    active_code = forms.CharField(max_length=7, required=True,
                                widget=forms.TextInput(attrs={"id":"varify-code"}),
                                error_messages={'required':'فیلد کدتایید نباید خالی باشد'})
    
    def clean_active_code(self):
        active_code = self.cleaned_data['active_code']
        
        if active_code == '':
            raise ValidationError('کد تایید نمیتوند خالی باشد')
        
        return active_code
# _________________________________________________________________

class LoginUserForm(forms.Form):
    
    mobile_number = forms.CharField(max_length=11, required=True,
                                    widget=forms.TextInput(attrs={"id":"mobile-login"}),
                                    error_messages={'required':'فیلد موبایل نباید خالی باشد'})
    
    password = forms.CharField(max_length=32, required=True,
                                    widget=forms.PasswordInput(attrs={"id":"password-login"}),
                                    error_messages={'required':'فیلد پسورد نباید خالی باشد'})
    
# _________________________________________________________________

class PasswordRememberForm(forms.Form):
    mobile_number = forms.CharField(max_length=11, required=True,
                                    widget=forms.TextInput(attrs={"id":"mobile-remember"}),
                                    error_messages={'required':'فیلد موبایل نباید خالی باشد'})
    
# _________________________________________________________________

class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(max_length=32, required=True,
                                    widget=forms.PasswordInput(attrs={"id":"password1-change"}),
                                    error_messages={'required':'فیلد پسورد نباید خالی باشد'})
    
    password2 = forms.CharField(max_length=32, required=True,
                                    widget=forms.PasswordInput(attrs={"id":"password2-change"}),
                                    error_messages={'required':'فیلد تکرار پسورد نباید خالی باشد'})
    
    def clean_password2(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']
        
        if pass1 and pass2 and pass1!=pass2:
            raise ValidationError('رمزعبور با تکرار آن برابر نمی باشد.')
            
        elif len(pass2) < 8:
            raise ValidationError('رمز عبور نمیتواند کمتر از 8 کاراکتر باشد')
        
        elif not re.findall(r'[0-9]',pass2):
            raise ValidationError('رمز عبور باید عدد داشته باشد')
        
        elif not re.findall(r'[a-z]',pass2):
            raise ValidationError('رمز عبور باید حداقل یک حرف کوچک داشته باشد')
        
        elif not re.findall(r'[A-Z]',pass2):
            raise ValidationError('رمز عبور باید حداقل یک حرف کوچک داشته باشد')
        
        elif not re.findall(r'[@#$%!^&*]',pass2):
            raise ValidationError('رمز عبور باید حداقل یک کاراکتر خاص داشته باشد (@#$%!^&*)')
        
        return pass2

# _________________________________________________________________

class UserPanelForm(forms.Form):
    first_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'id':'first-name'}),
                                 error_messages={'required':'فیلد نام اجباری است'})
    
    last_name = forms.CharField(max_length=70,widget=forms.TextInput(attrs={'id':'last-name'}),
                                 error_messages={'required':'فیلد نام خوانوادگی اجباری است'})
    
    email_account = forms.EmailField(max_length=70,widget=forms.EmailInput(attrs={'id':'email-account'}),
                                 error_messages={'required':'فیلد نام خوانوادگی اجباری است'})
    
    GENDER_CHOICES = [
        ('man','مرد'),
        ('female','زن'),
    ]
    
    gender = forms.ChoiceField(initial='man', choices=GENDER_CHOICES,
                               widget=forms.RadioSelect())
    
    postal_code = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'id':'postal-code'}),
                             error_messages={'required':'فیلد کدپستی اجباری است'})
    
    address = forms.CharField(max_length=300, widget=forms.TextInput(attrs={'id':'address-account','style':'height:100px'}),
                              error_messages={'required':'فیلد آدرس اجباری است'})
    
    mobile_number = forms.CharField(max_length=11,widget=forms.TextInput(attrs={'id':'mobile_number','readonly':'readonly'}),)
    
    phone_number = forms.CharField(max_length=11,widget=forms.TextInput(attrs={'id':'phone-number'}),
                                   error_messages={'required':'فیلد تلفن ثابت اجباری است'})
# _________________________________________________________________
