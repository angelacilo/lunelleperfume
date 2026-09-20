from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "contact", "payment_method", "user", "status", "created_at"]
    list_filter = ["status", "payment_method", "created_at"]
    search_fields = ["full_name", "contact", "note"]
    inlines = [OrderItemInline]
