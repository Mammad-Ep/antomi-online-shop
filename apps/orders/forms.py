from my_modules import forms
from .models import PaymentType
# _________________________________________________________________

class CouponForm(forms.Form):
    coupon = forms.CharField(max_length=20, required=False,
                             widget=forms.TextInput(attrs={"placeholder":"کد تخفیف",}))
# _________________________________________________________________

class CheckoutForm(forms.Form):
    fname = forms.CharField(max_length=50, required=True,
                            widget=forms.TextInput(),error_messages={'required':'فیلد نام اجباری است'})
    
    lname = forms.CharField(max_length=50, required=True,
                            widget=forms.TextInput(),error_messages={'required':'فیلد نام خانوادگی اجباری است'})
    
    address = forms.CharField(max_length=700, required=True,
                            widget=forms.Textarea(attrs={"placeholder":"نام شهر، میدان ، خیایان ، پلاک و ..."}),
                            error_messages={'required':'فیلد آدرس اجباری است'})
    
    postal_code = forms.CharField(max_length=10, required=True,
                            widget=forms.TextInput(),error_messages={'required':'فیلد کدپستی اجباری است'})
    
    phone_number = forms.CharField(max_length=11, required=True,
                            widget=forms.TextInput(attrs={"placeholder":"021********" ,"dir":"ltr"}),error_messages={'required':'فیلد تلفن اجباری است'})
    
    email = forms.EmailField(max_length=100, required=True,
                            widget=forms.EmailInput(attrs={"dir":"ltr"}),error_messages={'required':'فیلد ایمیل اجباری است'})
    
    mobile_number = forms.CharField(max_length=11, required=True,
                            widget=forms.TextInput(attrs={"readonly":"readonly"}),error_messages={'required':'فیلد نلفن همراه اجباری است'})
    
    description = forms.CharField(max_length=500, required=False,
                                  widget=forms.Textarea(attrs={"placeholder":"یادداشت های مربوط به سفارش، مانند توضیح نحوه ارسال."}),)
    
    payment_type = forms.ChoiceField(choices=[(item.id,item ) for item in PaymentType.objects.all()], required=True,
                                     widget=forms.RadioSelect())
# _________________________________________________________________
