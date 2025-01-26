from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    path('', Index.as_view(),name='index'),
    path('error404/', handler404,name='error404'),

]
