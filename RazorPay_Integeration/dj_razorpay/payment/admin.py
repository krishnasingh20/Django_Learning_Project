from django.contrib import admin
from .models import Payment

# Register your models here.
@admin.register(Payment)
class PaymentModel(admin.ModelAdmin):
    list_display = ('razorpay_payment_id', 'razorpay_order_id', 'amount', 'status')