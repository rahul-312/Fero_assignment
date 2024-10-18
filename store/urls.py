from django.urls import path
from .views import (
    CustomerListCreateView,
    CustomerUpdateView,
    ProductListCreateView,
    OrderListCreateView,
    OrderUpdateView,
    OrderFilterByProductView,
    OrderFilterByCustomerView
)

urlpatterns = [
    path('customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('customers/<int:pk>/', CustomerUpdateView.as_view(), name='customer-update'),
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderUpdateView.as_view(), name='order-update'),
    path('orders/filter/', OrderFilterByProductView.as_view(), name='order-filter'),
    path('orders/by-customer/',OrderFilterByCustomerView.as_view(),name='order-filter-by-customer')
]
