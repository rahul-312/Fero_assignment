from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255, unique=True)
    contact_number = models.CharField(max_length=15, null=False)
    email = models.EmailField(unique=True, null=False)

    
    created_dt = models.DateTimeField(auto_now_add=True, null=False)
    updated_dt = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        db_table = 'customer'
        indexes = [
            models.Index(fields=['customer_name'], name='customer_name_idx'),  # Index -> customer_name_idx
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(contact_number__regex=r'^\d{10,15}$'), name='customer_contact_number_cc')  # Check constraint -> customer_contact_number_cc
        ]
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.customer_name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255, unique=True, null=False)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=False)

    created_dt = models.DateTimeField(auto_now_add=True, null=False)
    updated_dt = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        db_table = 'product'
        indexes = [
            models.Index(fields=['product_name'], name='product_name_idx'),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(weight__gt=0, weight__lte=25), name='product_weight_cc')
        ]
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def clean(self):
        if self.weight <= 0 or self.weight > 25:
            raise ValidationError("Weight must be positive and less than or equal to 25kg.")

    def __str__(self):
        return self.product_name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)  # Primary key -> order_id
    order_number = models.CharField(max_length=10, unique=True, editable=False, null=False)  # Auto-generated unique order number
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='customer_id', null=False)  # Foreign Key -> NN
    order_date = models.DateField(null=False)  # Not Null -> NN
    order_address = models.CharField(max_length=255, null=False)  # Not Null -> NN

    
    created_dt = models.DateTimeField(auto_now_add=True, null=False)
    updated_dt = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        db_table = 'order'
        indexes = [
            models.Index(fields=['order_number'], name='order_number_idx'),  # Index -> order_number_idx
        ]
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = Order.objects.all().order_by('order_id').last()
            if last_order:
                new_order_number = int(last_order.order_number[3:]) + 1
            else:
                new_order_number = 1
            self.order_number = f'ORD{new_order_number:05d}'
        if self.order_date < date.today():
            raise ValidationError("Order date cannot be in the past.")
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, db_column='order_id', null=False, related_name='order_items')  # Ensure related_name is set for reverse lookup
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id', null=False)
    product_quantity = models.PositiveIntegerField(null=False)

    created_dt = models.DateTimeField(auto_now_add=True, null=False)
    updated_dt = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        db_table = 'order_item'
        indexes = [
            models.Index(fields=['order_id', 'product_id'], name='order_item_idx'),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(product_quantity__gt=0), name='order_item_quantity_cc'),
        ]
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"Order {self.order_id} - Product {self.product_id}"
