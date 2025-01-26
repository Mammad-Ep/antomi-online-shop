from django.shortcuts import render,redirect
from apps.orders.models import Order,OrderState
from apps.accounts.models import Customer
from apps.warehouses.models import SalesWarehouse
from my_modules import get_object_or_404
from my_modules import login_required
from my_modules import View
from my_modules import json
from my_modules import requests
from my_modules import HttpResponse
from my_modules import ObjectDoesNotExist
from my_modules import LoginRequiredMixin
from .models import Payment
# _________________________________________________________________

MERCHANT = '63C19DF7-ACFA-447B-9458-70F65B9C1025'
ZP_API_REQUEST = "https://sandbox.banktest.ir/zarinpal/api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://sandbox.banktest.ir/zarinpal/api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://sandbox.banktest.ir/zarinpal/www.zarinpal.com/pg/StartPay/{authority}"

CallbackURL = 'http://127.0.0.1:8000/payments/verify/'

class PaymentRequest(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            customer = Customer.objects.get(user=user)
            order = Order.objects.get(slug=kwargs['slug'])
            payment = Payment.objects.create(
               customer = customer,
               order = order,
               invoice_amount = order.invoice_amount,
               description = 'پرداخت از طریق درگاه پرداخت زرین پال' 
            )
            
            request.session['payment_session']={
                'order_id':order.id,
                'payment_id':payment.id,
            }
            
            req_data = {
                "merchant_id": MERCHANT,
                "amount": payment.invoice_amount * 10,
                "callback_url": CallbackURL,
                "description": payment.description,
                "metadata": {"mobile": user.mobile_number, "email": user.email}
            }
            req_header = {"accept": "application/json",
                        "content-type": "application/json'"}
            req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
                req_data), headers=req_header)
            authority = req.json()['data']['authority']
            if len(req.json()['errors']) == 0:
                return redirect(ZP_API_STARTPAY.format(authority=authority))
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
        except:
            return redirect('orders:checkout_cart',slug=kwargs['slug'])

# _________________________________________________________________

class PaymentVerify(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        payment_session = request.session.get('payment_session')
        order = Order.objects.get(id=payment_session['order_id'])
        payment = Payment.objects.get(id=payment_session['payment_id'])
        
        try:            
            t_status = request.GET.get('Status')
            t_authority = request.GET['Authority']
            if request.GET.get('Status') == 'OK':

                req_header = {"accept": "application/json",
                            "content-type": "application/json'"}
                req_data = {
                    "merchant_id": MERCHANT,
                    "amount": payment.invoice_amount * 10,
                    "authority": t_authority
                }
                req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
                if len(req.json()['errors']) == 0:
                    t_status = req.json()['data']['code']
                    if t_status == 100:
                        
                        order.is_finaly = True
                        order.order_state_id = 1
                        order.payment_type_id = 2
                        order.save()
                        
                        payment.is_finaly = True
                        payment.ref_id = str(req.json()['data']['ref_id'])
                        payment.status_code = t_status
                        payment.save()
                        
                        for item in order.order_details.all():
                            SalesWarehouse.objects.create(
                                user_registred = request.user,
                                product = item.product,
                                sale_price = item.price,
                                qty = item.qty
                            )
                        
                        request.session['payment_result']={
                            'order_slug':order.slug,
                            'payment_type':'online',
                            'ref_id':payment.ref_id,
                            'message':''
                        } 
                          
                        del request.session['shop_cart'] 
                        del request.session['payment_session'] 
                        temp = request.session.get('coupon_session')
                        if temp:
                            del request.session['coupon_session'] 
                        
                        return redirect('payments:payment_result')

                    elif t_status == 101:
                        order.is_finaly = True
                        order.order_state_id = 1
                        order.payment_type_id = 2
                        order.save()
                        
                        payment.is_finaly = True
                        payment.ref_id = str(req.json()['data']['ref_id'])
                        payment.status_code = t_status
                        payment.save()
                        
                        for item in order.order_details.all():
                            SalesWarehouse.objects.create(
                                user_registred = request.user,
                                product = item.product,
                                sale_price = item.price,
                                qty = item.qty
                            )
                        
                        request.session['payment_result']={
                            'order_slug':order.slug,
                            'payment_type':'online',
                            'ref_id':payment.ref_id,
                            'message':''
                        } 
                          
                        del request.session['shop_cart'] 
                        del request.session['payment_session']  
 
                        temp = request.session.get('coupon_session')
                        if temp:
                            del request.session['coupon_session'] 
                        
                        return redirect('payments:payment_result')
                        # return HttpResponse('Transaction submitted : ' + str(req.json()['data']['message']))
                    else:
                        request.session['payment_result']={
                            'order_slug':order.slug,
                            'payment_type':'failed',
                            'message':str(req.json()['data']['message']),
                            'ref_id':''
                        } 
                        del request.session['shop_cart'] 
                        del request.session['payment_session'] 
                        temp = request.session.get('coupon_session')
                        if temp:
                            del request.session['coupon_session'] 
                        
                        return redirect('payments:payment_result')
                        # return HttpResponse('Transaction failed.\nStatus: ' + str(req.json()['data']['message']))
                else:
                    e_code = req.json()['errors']['code']
                    e_message = req.json()['errors']['message']
                    
                    request.session['payment_result']={
                        'order_slug':order.slug,
                        'payment_type':'failed',
                        'message':e_message,
                        'ref_id':''
                    } 
                    
                    del request.session['shop_cart'] 
                    del request.session['payment_session'] 
                    temp = request.session.get('coupon_session')
                    if temp:
                        del request.session['coupon_session'] 
                        
                    return redirect('payments:payment_result')
                    # return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
            else:
                
                request.session['payment_result']={
                    'order_slug':order.slug,
                    'payment_type':'failed',
                    'message':'تراکنش با خطا مواجه شد.',
                    'ref_id':''
                } 
                
                del request.session['shop_cart'] 
                del request.session['payment_session']  
                temp = request.session.get('coupon_session')
                if temp:
                    del request.session['coupon_session'] 
                
                return redirect('payments:payment_result')
                # return HttpResponse('Transaction failed or canceled by user')
        except:
            return redirect('orders:checkout_cart',order.slug)
# _________________________________________________________________

class PaymentResult(LoginRequiredMixin,View):
    
    def get(self, request, *args, **kwargs):
        payment_result = request.session['payment_result']
        order = get_object_or_404(Order,slug=payment_result['order_slug'])
        payment_type = payment_result['payment_type']
        customer = Customer.objects.get(user=request.user)
        
        context = {
            'order':order,
            'payment_type':payment_type,
            'customer':customer,
            'ref_id':payment_result['ref_id'],
            'message':payment_result['message']
        }
        return render(request,'payments_app/payment_result.html',context)
# _________________________________________________________________
