from rest_framework import serializers
from .models import Customer, Product, Order, OrderItem
from datetime import date


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'customer_id', 'customer_name', 'contact_number', 'email', 
            'created_dt', 'updated_dt'
        ]
        read_only_fields = ['created_dt', 'updated_dt']

    def __init__(self, *args, **kwargs):
        super(CustomerSerializer, self).__init__(*args, **kwargs)
        if self.instance:  # If it's an update (instance exists)
            for field in self.fields:
                self.fields[field].required = False


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'product_id', 'product_name', 'weight', 
             'created_dt', 'updated_dt'
        ]
        read_only_fields = ['created_dt', 'updated_dt']



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product_id', 'product_quantity']
        read_only_fields = ['created_dt', 'updated_dt']

    def validate_product_quantity(self, value):
        """Ensure that the product quantity is greater than 0."""
        if value <= 0:
            raise serializers.ValidationError("Product quantity must be greater than zero.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = [
            'order_id', 'order_number', 'customer_id', 'order_date', 'order_address',
            'created_dt', 'updated_dt', 'order_items'
        ]
        read_only_fields = ['order_number', 'created_dt', 'updated_dt']

    def validate_order_date(self, value):
        """Ensure that order date is not in the past."""
        if value < date.today():
            raise serializers.ValidationError("Order date cannot be in the past.")
        return value

    def validate(self, data):
        """Ensure the total weight of the order does not exceed 150kg."""
        order_items_data = data.get('order_items', [])
        total_weight = 0

        # Calculate the total weight of all order items
        for item_data in order_items_data:
            product = item_data['product_id']  # Get the product instance
            product_quantity = item_data['product_quantity']
            total_weight += product.weight * product_quantity  # Assuming product model has a weight field

        if total_weight > 150:
            raise serializers.ValidationError("The total weight of the order cannot exceed 150kg.")

        return data

    def create(self, validated_data):
        # Extract the nested order_items from validated data
        order_items_data = validated_data.pop('order_items')
        
        # Create the Order
        order = Order.objects.create(**validated_data)
        
        # Create each OrderItem related to the order
        for item_data in order_items_data:
            OrderItem.objects.create(order_id=order, **item_data)
        
        return order
    
    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('order_items', None)
        instance.order_address = validated_data.get('order_address', instance.order_address)
        instance.save()
        if order_items_data is not None:
            instance.order_items.all().delete()
            for item_data in order_items_data:
                OrderItem.objects.create(order_id=instance, **item_data)
        return instance