from django.urls import path
from .views import *
# _________________________________________________________________

app_name = 'scorings'

urlpatterns = [
    path('scorings_partial/<slug:slug>', scorings_partial ,name='scorings_partial'),
    path('add_score/', add_score ,name='add_score'),

]

# _________________________________________________________________
