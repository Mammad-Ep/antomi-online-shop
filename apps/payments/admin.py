from django.contrib import admin
from .models import Payment
# _________________________________________________________________

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('customer','order','is_finaly','ref_id','status_code','invoice_amount','register_date','update_date')
    list_filter = ('customer',)
    search_fields = ('ref_id',)
    ordering = ('-register_date',)
    list_editable = ('is_finaly',)


# _________________________________________________________________