from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('order/', create_order, name='create_order'),
    path('paymenthandler/', handlePayment, name='handlePayment'),
]