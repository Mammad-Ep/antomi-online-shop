from django.contrib import admin
from .models import DiscountBasket,DiscountCoupon,DiscountBasketDetails
# _________________________________________________________________

@admin.register(DiscountCoupon)
class DiscountCouponAdmin(admin.ModelAdmin):
    list_display = ('coupon_title','discount','is_active','start_date','end_date')
    list_filter = ('coupon_title',)
    search_fields = ('coupon_title',)
    list_editable = ('is_active',)
# _________________________________________________________________

class DiscountBasketDetailsInline(admin.TabularInline):
    model = DiscountBasketDetails
    extra = 13

@admin.register(DiscountBasket)
class DiscountBasketAdmin(admin.ModelAdmin):
    list_display = ('discount_basket_title','is_active','discount','start_date','end_date')
    list_filter = ('discount_basket_title',)
    search_fields = ('discount_basket_title',)
    list_editable = ('is_active',)
    inlines = [DiscountBasketDetailsInline,]
# _________________________________________________________________
