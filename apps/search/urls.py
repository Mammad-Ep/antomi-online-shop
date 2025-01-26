from django.urls import path
from .views import *
# _________________________________________________________________

app_name = 'search'

urlpatterns = [
    path('search_box_area', search_box_area ,name='search_box_area'),
    path('search/', SearchView.as_view() ,name='search'),

]

# _________________________________________________________________
