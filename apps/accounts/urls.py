from django.urls import path
from .views import *
# _________________________________________________________________

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterUserView.as_view(),name='register'),
    path('verify/', VerifyUserView.as_view(),name='verify'),
    path('login/', LoginUserView.as_view(),name='login'),
    path('logout/', LogOutUserView.as_view(),name='logout'),
    path('password_remember/', PasswordRememberView.as_view(),name='password_remember'),
    path('change_password/', ChangePasswordView.as_view(),name='change_password'),
    path('send_sms_again/', send_sms_again,name='send_sms_again'),
    
    path('userpanel/', UserPanelView.as_view() , name='userpanel'),
    path('user_info/', user_info , name='user_info'),
    path('last_orders_user/', last_orders_user,name='last_orders_user'),
    path('last_payments_user/', last_payments_user,name='last_payments_user'),
    path('account_details/', account_details,name='account_details'),

]

# _________________________________________________________________
