from django.urls import path
from .views import *
# _________________________________________________________________

app_name = 'comments'

urlpatterns = [
    path('create_comment_product/<slug:slug>', create_comment_product ,name='create_comment_product'),
    path('create_comment_child/', create_comment_child ,name='create_comment_child'),
    path('like_comment_partial/<int:id>', like_comment_partial ,name='like_comment_partial'),
    path('add_like_comment/', add_like_comment ,name='add_like_comment'),


]

# _________________________________________________________________
