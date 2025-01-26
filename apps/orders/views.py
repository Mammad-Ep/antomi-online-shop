from django.shortcuts import render,redirect
from my_modules import get_object_or_404
from my_modules import View
from my_modules import HttpResponse
from my_modules import messages
from my_modules import Q
from my_modules import datetime
from my_modules import ObjectDoesNotExist
from my_modules import login_required
from my_modules import LoginRequiredMixin
from apps.products.models import Product
from apps.accounts.models import Customer
from apps.discounts.models import DiscountCoupon
from apps.payments.models import Payment
from apps.warehouses.models import SalesWarehouse
from .shop_cart import ShopCart
from utils import get_price_delivery_tax
from .forms import CouponForm,CheckoutForm
from .models import Order,orderDetails,PaymentType,OrderState
import utils
# _________________________________________________________________

class ShopCartView(View):
    template_name = 'orders_app/shop_cart.html'
    def get(self, request, *args, **kwargs):
        shop_cart = ShopCart(request)
        return render(request,self.template_name,{'shop_cart':shop_cart})
# _________________________________________________________________

def show_shop_cart(request):
    shop_cart = ShopCart(request)
    final_price = shop_cart.get_final_price()
    discount = 0
    discount_session = request.session.get('coupon_session')
    if discount_session:
        discount = discount_session['discount']
        
    order_final_price,tax,delivery = get_price_delivery_tax(final_price,discount)
    coupon_form = CouponForm()
    
    
    context = {
        'shop_cart':shop_cart,
        'final_price':final_price,
        'order_final_price':order_final_price,
        'delivery':delivery,
        'tax':tax,
        'coupon_form':coupon_form,
        'discount':discount
    }
    
    return render(request,'orders_app/partials/show_shop_cart.html',context)
# _________________________________________________________________

def applay_coupon_cart(request):
    if request.method == "POST":
        coupon_form = CouponForm(request.POST)
        if coupon_form.is_valid():
            data = coupon_form.cleaned_data
            discount_coupon = DiscountCoupon.objects.filter(
                Q(coupon_title=data['coupon'])&
                Q(is_active=True)&
                Q(start_date__lte=datetime.now())&
                Q(end_date__gte=datetime.now())       
            )
            
            discount = 0
            if discount_coupon:
               discount = discount_coupon[0].discount 
               request.session['coupon_session']={'discount':discount}
               messages.success(request,'کد تخفیف اعمال شد','success')
               return redirect('orders:cart')
            
            request.session['coupon_session']={'discount':discount} 
            messages.warning(request,'کد وارد شده اشتباه است','warning')
            return redirect('orders:cart')
        messages.warning(request,'کد وارد شده معتبر نمی باشد','warning')
        return redirect('orders:cart')
            
# _________________________________________________________________

def add_shop_cart(request):
    product_id = request.GET.get('product_id')
    qty = request.GET.get('qty')
    
    product = get_object_or_404(Product,id=product_id)
    shop_cart = ShopCart(request)
    shop_cart.add_shop_cart(product,qty)
    
    return HttpResponse('success')
      
# _________________________________________________________________

def remove_shop_cart(request):
    product_id = request.GET.get('product_id')
    
    product = get_object_or_404(Product,id=product_id)
    shop_cart = ShopCart(request)
    shop_cart.remove_shop_cart(product)
    
    return redirect('orders:show_shop_cart')
# _________________________________________________________________

def update_shop_cart(request):
    product_id = request.GET.get('product_id')
    qty = request.GET.get('qty')
    
    product = get_object_or_404(Product,id=product_id)
    shop_cart = ShopCart(request)
    shop_cart.update_shop_cart(product,qty)
    
    return redirect('orders:show_shop_cart')
# _________________________________________________________________

def status_shop_cart(request):
    shop_cart = ShopCart(request)
    return HttpResponse(shop_cart.count)
# _________________________________________________________________

@login_required(login_url='/login/')
def create_order(request):
    try:
       customer =  Customer.objects.get(user=request.user)
    except ObjectDoesNotExist:
        customer = Customer.objects.create(user=request.user)
    
    discount = 0
    discount_session = request.session.get('coupon_session')
    if discount_session:
        discount = discount_session['discount']
        
    shop_cart = ShopCart(request)    
    code = f'ant-{utils.get_random_code(7)}'
    order = Order.objects.create(customer=customer,order_code=code,order_state=OrderState.objects.get(id=5),discount=discount)
    
    
    for item in shop_cart:
        orderDetails.objects.create(
            product = item['product'],
            order = order,
            price = item['price_by_discount'],
            qty = item['qty']
        )
        
    return redirect('orders:checkout_cart',order.slug)
    
    
# _________________________________________________________________

class CheckoutCart(View,LoginRequiredMixin):
    template_name = 'orders_app/checkout_cart.html'
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order,slug=kwargs['slug'])
        user = request.user
        customer = get_object_or_404(Customer,user=user)
        
        shop_cart = ShopCart(request)  
        final_price = shop_cart.get_final_price()
        order_final_price,tax,delivery = get_price_delivery_tax(final_price,order.discount)
        
        initial_dict = {
            'fname':user.name,
            'lname':user.family,
            'address':customer.address,
            'postal_code':customer.postal_code,
            'phone_number':customer.phone_number,
            'email':user.email,
            'mobile_number':user.mobile_number,
            'description':order.description,

        }
        
        form = CheckoutForm(initial=initial_dict)
        
        context = {
            'form':form,
            'shop_cart':shop_cart,
            'final_price':final_price,
            'order_final_price':order_final_price,
            'delivery':delivery,
            'tax':tax,
            'discount':order.discount
        }
        return render(request,self.template_name,context)
    
    
    def post(self, request, *args, **kwargs):
        form = CheckoutForm(request.POST)
        order = get_object_or_404(Order,slug=kwargs['slug'])
        if form.is_valid():
            data = form.cleaned_data
            user = request.user
            customer = get_object_or_404(Customer,user=user)
            shop_cart = ShopCart(request)  
            final_price = shop_cart.get_final_price()
            order_final_price,tax,delivery = get_price_delivery_tax(final_price,order.discount)
            
            order.description = data['description']
            order.invoice_amount = order_final_price
            order.payment_type = PaymentType.objects.get(id=data['payment_type'])
            order.save()
            
            customer.phone_number = data['phone_number']
            customer.postal_code = data['postal_code']
            customer.address = data['address']
            customer.save()
            
            user.name = data['fname']
            user.family = data['lname']
            user.email = data['email']
            user.save()
            
            if order.payment_type_id == 1:
                order.is_finaly = True
                order.order_state = OrderState.objects.get(id=1)
                order.payment_type = PaymentType.objects.get(id=1)
                order.save()
                
                Payment.objects.create(
                    customer = customer,
                    order = order,
                    is_finaly = True,
                    invoice_amount = order.invoice_amount,
                    description = 'پرداخت درب منزل'
                )
                
                for item in shop_cart:
                    SalesWarehouse.objects.create(
                        user_registred = user,
                        product = item['product'],
                        sale_price = item['price_by_discount'],
                        qty = item['qty']
                    )
                    
                request.session['payment_result']={
                    'order_slug':order.slug,
                    'payment_type':'at_home',
                    'ref_id':'',
                    'message':''
                }
                
                del request.session['shop_cart'] 
                temp = request.session.get('coupon_session')
                if temp:
                    del request.session['coupon_session'] 
                   
                return redirect('payments:payment_result')
            
            if order.payment_type_id == 2:              
                return redirect('payments:request',order.slug)
            
        return redirect('orders:checkout_cart',order.slug)

# _________________________________________________________________