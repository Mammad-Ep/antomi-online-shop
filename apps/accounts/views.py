from django.shortcuts import render,redirect
from my_modules import View
from my_modules import LoginRequiredMixin
from my_modules import messages
from my_modules import authenticate
from my_modules import login
from my_modules import logout
from my_modules import login_required
from my_modules import get_object_or_404
from my_modules import ObjectDoesNotExist
from .forms import (RegisterUserForm,CaptchaTestForm,VerifyUserForm,
                    LoginUserForm,PasswordRememberForm,ChangePasswordForm,UserPanelForm)
from .models import CustomUser
from .models import Customer
import utils
from apps.orders.models import Order
from apps.payments.models import Payment
# _________________________________________________________________

class RegisterUserView(View):
    template_name = 'accounts_app/register.html'
    
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = RegisterUserForm()
        form_captcha = CaptchaTestForm()
        context = {
            'form':form,
            'form_captcha':form_captcha
        }
        return render(request,self.template_name,context)
    
    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        form_captcha = CaptchaTestForm(request.POST)
        if form_captcha.is_valid():  
            if form.is_valid():
                data = form.cleaned_data
                user = CustomUser.objects.filter(mobile_number = data['mobile_number'])
                if not user:                    
                    active_code = utils.get_random_code(7)
                    utils.send_sms(data['mobile_number'],f'کد تایید ثبت نام شما : {active_code}')
                    
                    request.session['user_session']={
                        'mobile_number':data['mobile_number'],
                        'pass':data['password2'],
                        'password_remember':False,
                        'active_code':str(active_code)
                    }
                    print(f'active_code =====> {active_code}')
                    messages.success(request,'پیش ثبت نام با موفقیت انجام شد','success')
                    return redirect('accounts:verify')
                else:
                    messages.warning(request,'قبلا با این شماره ثبت نام انجام شده است','warning')
                    return render(request,self.template_name,{'form':form,'form_captcha':form_captcha})
            else:
                return render(request,self.template_name,{'form':form,'form_captcha':form_captcha})    
        else:
            messages.error(request,'کد امنیتی واردشده معتبر نمی باشد','danger')
            return render(request,self.template_name,{'form':form,'form_captcha':form_captcha})       
                
# _________________________________________________________________

class VerifyUserView(View):
    template_name = 'accounts_app/verify.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request, *args, **kwargs):
        form = VerifyUserForm()       
        return render(request,self.template_name,{'form':form})
    
    def post(self, request, *args, **kwargs):
        form = VerifyUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_session=request.session.get('user_session')
            print(user_session)
            if user_session['active_code'] == data['active_code']:
                if user_session['password_remember'] == False:
                    user = CustomUser.objects.create(
                        mobile_number = user_session['mobile_number'],
                        active_code = utils.get_random_code(7)
                    )
                    
                    user.is_active = True
                    user.set_password(user_session['pass'])
                    user.save()
                    
                    del request.session['user_session']
                    messages.success(request,'ثبت نام با موفقیت انجام شد','success')
                    return redirect('main:index')
                else:
                    return redirect('accounts:change_password')
            else:
                messages.error(request,'کد تایید نادرست می باشد','danger')
                return render(request,self.template_name,{'form':form})
        else:
            # messages.error(request,'کد تایید نامعتبر می باشد','daner')
            return render(request,self.template_name,{'form':form})
# _________________________________________________________________

class LoginUserView(View):
    template_name = 'accounts_app/login.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = LoginUserForm()
        form_captcha = CaptchaTestForm()
        
        return render(request,self.template_name,{'form':form,'form_captcha':form_captcha})
    
    def post(self, request, *args, **kwargs):
        form_captcha = CaptchaTestForm(request.POST)
        form = LoginUserForm(request.POST)
        
        if form_captcha.is_valid():
            if form.is_valid():
                data = form.cleaned_data
                user = authenticate(username=data['mobile_number'],password=data['password'])
                
                if user is not None:
                    current_user = CustomUser.objects.get(mobile_number=data['mobile_number'])
                    if current_user.is_active == True:
                        if current_user.is_admin == False:
                            login(request,user)
                            messages.success(request,'ورود با موفقیت انجام شد','success')
                            next_url = request.GET.get('next')
                            if next_url is not None:
                                return redirect(next_url)
                            else:
                                return redirect('main:index')
                        
                        messages.warning(request,'کاربر ادمین نمیتواند از این بخش وارد شود','warning')
                        return render(request,self.template_name,{'form':form,'form_captcha':form_captcha})
                    
                    messages.warning(request,'کاربر موردنظر غیرفعال می باشد','warning')
                    return render(request,self.template_name,{'form':form,'form_captcha':form_captcha})
                
                messages.warning(request,'اصلاعاتی با این مشخصات یافت نشد','warning')
                # return render(request,self.template_name,{'form':form,'form_captcha':form_captcha})
            
            # messages.warning(request,'اصلاعات وارد شده معتبر نمی باشد','warning')
            return render(request,self.template_name,{'form':form,'form_captcha':form_captcha})
        
        messages.error(request,'کد امنیتی معتبر نمی باشد','danger')
        return render(request,self.template_name,{'form':form,'form_captcha':form_captcha})
            
# _________________________________________________________________

class LogOutUserView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs): 
        temp = request.session['shop_cart']
        logout(request)
        request.session['shop_cart'] = temp
        return redirect('main:index')    
# _________________________________________________________________

class PasswordRememberView(View):
    template_name = 'accounts_app/password_remember.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = PasswordRememberForm()
        form_captcha = CaptchaTestForm()
        
        return render(request,self.template_name,{'form_captcha':form_captcha,'form':form})


    def post(self, request, *args, **kwargs):
        form = PasswordRememberForm(request.POST)
        form_captcha = CaptchaTestForm(request.POST)
        
        if form_captcha.is_valid():
            if form.is_valid():
                data = form.cleaned_data
                user = CustomUser.objects.filter(mobile_number=data['mobile_number'])
                if user:
                    active_code = utils.get_random_code(7)
                    utils.send_sms(data['mobile_number'],f'کدبازیابی رمز عبور شما : {active_code}')
                    
                    request.session['user_session']={
                        'mobile_number':data['mobile_number'],
                        'pass':'',
                        'password_remember':True,
                        'active_code':str(active_code)
                    }
                    print(f'active_code =====> {active_code}')
                    messages.success(request,'کد بازیابی برای شماره موبایل ارسال شد')
                    return redirect('accounts:verify')
                else:
                    messages.warning(request,'شماره موردنظر یافت نشد','warning')
                    return redirect('accounts:password_remember') 
            else:
                messages.warning(request,'اصلاعاتی با این مشخصات یافت نشد','warning')
                return redirect('accounts:password_remember')
        else:
            messages.error(request,'کد امنیتی معتبر نمی باشد','danger')
            return render(request,self.template_name,{'form':form,'form_captcha':form_captcha})
# _________________________________________________________________

class ChangePasswordView(View):
    template_name = 'accounts_app/change_password.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = ChangePasswordForm()
        form_captcha = CaptchaTestForm()
        
        return render(request,self.template_name,{'form_captcha':form_captcha,'form':form})

    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(request.POST)
        form_captcha = CaptchaTestForm(request.POST)
        
        if form_captcha.is_valid():
            if form.is_valid():
                data = form.cleaned_data
                user_session = request.session.get('user_session')
                user = CustomUser.objects.get(mobile_number=user_session['mobile_number'])
                if not user.check_password(data['password2']):
                    user.active_code = utils.get_random_code(7)
                    user.set_password(data['password2'])
                    user.save()
                    del request.session['user_session']
                    messages.success(request,'رمز عبور با موفقیت تغییر کرد','success')
                    return redirect('accounts:login')
                else:
                    messages.warning(request,'از این رمزعبور قبلا استفاده شده است','warning')
                    return redirect('accounts:change_password')
            else:
                return render(request,self.template_name,{'form':form,'form_captcha':form_captcha})
        else:
            messages.error(request,'کد امنیتی معتبر نمی باشد','danger')
            return render(request,self.template_name,{'form':form,'form_captcha':form_captcha})

# _________________________________________________________________

def send_sms_again(request):
    active_code = utils.get_random_code(7)
    user_session = request.session.get('user_session')
    mobile_number = user_session['mobile_number']
    utils.send_sms(mobile_number,f'کد تایید مجدد شما: {active_code}')
    print(f'active_code =====> {active_code}')
    
    request.session['user_session']={
        'mobile_number':mobile_number,
        'pass':user_session['pass'],
        'password_remember':user_session['password_remember'],
        'active_code':str(active_code)
    }
    

    return redirect("accounts:verify")
# _________________________________________________________________

### UserPanel

class UserPanelView(LoginRequiredMixin,View):
    login_url='/login/'
    redirect_field_name='login' 
    template_name = 'accounts_app/userpanel.html'
    
    def get(self, request, *args, **kwargs):
        
        return render(request,self.template_name)
# _________________________________________________________________

@login_required(login_url='/login/')
def user_info(request):
    try:
        user = request.user
        customer = Customer.objects.get(user=user)
        
        context = {
            'name':user.name,
            'family':user.family,
            'email':user.email,
            'mobile':user.mobile_number,
            'address':customer.address,
            'postal_code':customer.postal_code            
        }
    except:
            user = request.user
            context = {
            'fullname':f'{user.name} {user.family}',
            'email':user.email,
            'mobile':user.mobile_number,       
        }
    
    return render(request,'accounts_app/partials/user_info.html',context)
# _________________________________________________________________

@login_required(login_url='/login/')
def last_orders_user(request):
    try:
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer).order_by('-register_date')[:7]
    
    except ObjectDoesNotExist:
        orders = []
    
    return render(request,'accounts_app/partials/last_orders_user.html',{'orders':orders})
        
        
# _________________________________________________________________

@login_required(login_url='/login/')
def last_payments_user(request):
    try:
        customer = Customer.objects.get(user=request.user)
        payments = Payment.objects.filter(customer=customer).order_by('-register_date')[:7]
    
    except ObjectDoesNotExist:
        payments = []
        
    return render(request,'accounts_app/partials/last_payments_user.html',{'payments':payments})
# _________________________________________________________________

@login_required(login_url='/login/',redirect_field_name='login')
def account_details(request):
    if request.method == "GET":
        try:
            user = request.user
            customer = Customer.objects.get(user=user)
            
            initial_dict = {
               'first_name':user.name, 
               'last_name':user.family, 
               'email_account':user.email, 
               'mobile_number':user.mobile_number,
               'gender':user.gender,
               'phone_number':customer.phone_number,
               'postal_code':customer.postal_code,
               'address':customer.address, 
            }
            
        except:
                user = request.user
                
                initial_dict = {
                'first_name':user.name, 
                'last_name':user.family, 
                'email_account':user.email, 
                'mobile_number':user.mobile_number,
                'gender':user.gender,

                } 
                        
        form = UserPanelForm(initial=initial_dict)
        return render(request,'accounts_app/partials/account_details.html',{'form':form})
    
    
    if request.method == "POST":
        form = UserPanelForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = request.user
            try: 
                customer = Customer.objects.get(user=user)
            except:
                customer = Customer.objects.create(user=user)
                
            user = request.user
            customer = Customer.objects.get(user=user)
            user.name = data['first_name']
            user.family = data['last_name']
            user.email = data['email_account']
            user.gender = data['gender']
            user.save()
            
            customer.postal_code = data['postal_code']
            customer.address = data['address']
            customer.phone_number = data['phone_number']
            customer.save()
                
            messages.success(request,'اطلاعات پنل کاربری با موفقیت بروزرسانی شد','success')
            return redirect('accounts:userpanel')
        
        return render(request,'accounts_app/partials/account_details.html',{'form':form})    
        
# _________________________________________________________________


