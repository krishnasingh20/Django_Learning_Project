from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('/send_pdf/', send_pdf, name='send_pdf')
]