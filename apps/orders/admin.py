from django.contrib import admin
from .models import Order,OrderState,PaymentType,orderDetails
# _________________________________________________________________


class orderDetailsInline(admin.TabularInline):
    model = orderDetails
    extra = 3

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer','order_code','is_finaly','slug','discount','invoice_amount','register_date','update_date')
    list_filter = ('customer',)
    search_fields = ('order_code',)
    ordering = ('-register_date',)
    list_editable = ('is_finaly',)
    inlines = (orderDetailsInline,)

# _________________________________________________________________

@admin.register(OrderState)
class OrderStateAdmin(admin.ModelAdmin):
    list_display = ('id','order_state_title',)
    list_filter = ('order_state_title',)
    search_fields = ('order_state_title',)
    

# _________________________________________________________________

@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('payment_type_title',)
    list_filter = ('payment_type_title',)
    search_fields = ('payment_type_title',)
    

# _________________________________________________________________

