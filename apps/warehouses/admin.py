from django.contrib import admin
from .models import SalesWarehouse,PurchaseWarehouse
# _________________________________________________________________

@admin.register(SalesWarehouse)
class SalesWarehouseAdmin(admin.ModelAdmin):
    list_display = ('user_registred','product','sale_price','qty','register_date','update_date')
    list_filter = ('product',)
    search_fields = ('product',)
    ordering = ('-update_date',)
# _________________________________________________________________

@admin.register(PurchaseWarehouse)
class PurchaseWarehouseAdmin(admin.ModelAdmin):
    list_display = ('user_registred','product','purchase_price','qty','register_date','update_date')
    list_filter = ('product',)
    search_fields = ('product',)
    ordering = ('-update_date',)
# _________________________________________________________________
