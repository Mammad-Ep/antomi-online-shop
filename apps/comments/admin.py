from django.contrib import admin
from .models import CommentProduct
# _________________________________________________________________

@admin.register(CommentProduct)
class CommentProductAdmin(admin.ModelAdmin):
    list_display = ('user_commenter','is_active','user_confirming','register_date','update_date','fullname','email','comment_parent')
    list_editable = ('is_active',)
    list_filter = ('user_commenter',)
    ordering = ('-register_date',)
    search_fields = ('user_commenter',)
# _________________________________________________________________
