from django.contrib import admin
from .models import Favorites
# _________________________________________________________________

@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('favorite_user','product','register_date')
    search_fields = ('product',)
    list_filter = ('product',)
    ordering = ('register_date',)
# _________________________________________________________________
