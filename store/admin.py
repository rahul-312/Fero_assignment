from django.contrib import admin
from .models import Customer, Product, Order, OrderItem

# Customer Admin
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_id', 'customer_name', 'contact_number', 'email', 'created_dt']
    search_fields = ['customer_name', 'email', 'contact_number']
    list_filter = ['created_dt', 'updated_dt']
    readonly_fields = ['created_dt', 'updated_dt']

# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'product_name', 'weight', 'created_dt']
    search_fields = ['product_name']
    list_filter = ['created_dt', 'updated_dt']
    readonly_fields = ['created_dt', 'updated_dt']

# Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'order_number', 'customer_id', 'order_date', 'order_address',  'created_dt']
    search_fields = ['order_number', 'customer_id__customer_name', 'order_address']
    list_filter = ['order_date', 'created_dt', 'updated_dt']
    readonly_fields = ['order_number', 'created_dt', 'updated_dt']

# OrderItem Admin
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order_item_id', 'order_id', 'product_id', 'product_quantity',  'created_dt']
    search_fields = ['order_id__order_number', 'product_id__product_name']
    list_filter = ['created_dt', 'updated_dt']
    readonly_fields = ['created_dt', 'updated_dt']
