from django.urls import path
from .views import *


urlpatterns = [
    path('dhs26/', home, name='home'),
    path('dhs26/speakers/', speakers, name='speaker'),
    path('dhs26/speakers/<int:id>/', speaker_detail, name='speaker_detail'),
    path('dhs26/sponsors/', sponsors, name='sponsors'),
    path('dhs26/sponsors/<int:id>/', sponsor_detail, name='sponsor_detail'),
    path('dhs26/sessions/', sessions, name='sessions'),
    path('dhs26/sessions/<int:id>/', session_detail, name='session_detail'),
    path('dhs26/workshops/<int:id>/', workshop_detail, name='workshop_detail'),
    path('dhs26/awards/', awards, name='awards'),
    path('dhs26/download_file/', download_file, name='download_file'),
    path('dhs26/download_woprkshop_detail/', send_workshop_detail, name='download_woprkshop_detail'),
    path('dhs26/emailAgenda/', emailAgenda, name='emailAgenda'),
    path('dhs26/checkout/buy_workshop/<int:id>/', buy_workshop, name="checkout_buy_workshop"),
    path('dhs26/checkout/conference/', checkout_conference, name='checkout_conference'),
    path('dhs26/checkout/conference-workshop/', checkout_conference_workshop, name='checkout_conference_workshop'),
    path('dhs26/create_order/', create_order, name='create_order'),
    path('dhs26/create_order_conference/', create_order_conference, name='create_order_conference'),
    path('dhs26/create_order_workshop/', create_order_workshop, name='create_order_workshop'),
    path('dhs26/handlePayment/', handlePayment, name='handlePayment'),
]