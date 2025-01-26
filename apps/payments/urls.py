from django.urls import path
from .views import *
# _________________________________________________________________

app_name = 'payments'

urlpatterns = [
    path('request/<slug:slug>', PaymentRequest.as_view(), name='request'),
    path('verify/', PaymentVerify.as_view() , name='verify'),
    path('payment_result/', PaymentResult.as_view() ,name='payment_result'),


]
# _________________________________________________________________
