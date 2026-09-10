from django.contrib import admin
from .models import *

@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ("name", "designation", "updated_at")
    search_fields = ("name", "designation")

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ("name", "type")
    list_filter = ("type",)
    search_fields = ("name", )

@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "price", "is_sold_out")
    list_editable = ("is_sold_out",)
    filter_horizontal = ("instructors",)

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("name", "type")
    filter_horizontal = ("speakers",)


@admin.register(DownloadDetail)
class DownloadDetailAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('razorpay_order_id', 'razorpay_payment_id', 'amount', 'status', 'payment_type')