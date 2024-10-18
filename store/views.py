from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Product, Order
from .serializers import CustomerSerializer, ProductSerializer, OrderSerializer


class CustomerListCreateView(APIView):
    """
        API view to retrieve and create Customer instances.

        This view provides the following functionalities:

        - **GET**: Retrieve a list of all customers.
            - Response: A JSON array containing customer details.
            - Status Code: 200 OK if successful.

        - **POST**: Create a new customer instance.
            - Request Body: A JSON object containing customer details.
            - Response: The created customer's details.
            - Status Codes:
                - 201 Created: If the customer is successfully created.
                - 400 Bad Request: If the request data is invalid.

        Attributes:
            request (Request): The incoming request.
    """
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerUpdateView(APIView):
    """
    API view to update an existing Customer instance.

    This view allows the following functionality:

    - **PUT**: Update an existing customer instance based on the provided primary key (pk).
        - Request Body: A JSON object containing the fields to be updated. Partial updates are allowed.
        - URL Parameter:
            - `pk`: The primary key of the customer to be updated.
        - Response: The updated customer's details.
        - Status Codes:
            - 200 OK: If the customer is successfully updated.
            - 404 Not Found: If the customer with the given primary key does not exist.
            - 400 Bad Request: If the request data is invalid.
    
    Attributes:
        request (Request): The incoming request.
        pk (int): The primary key of the customer instance to update.
    """
    def put(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListCreateView(APIView):
    """
    API view to retrieve and create Product instances.

    This view provides the following functionalities:
    
    - **GET**: Retrieve a list of all products.
        - Response: A JSON array containing product details.
        - Status Code: 200 OK if successful.
        
    - **POST**: Create a new product instance.
        - Request Body: A JSON object containing product details.
        - Response: The created product's details.
        - Status Codes:
            - 201 Created: If the product is successfully created.
            - 400 Bad Request: If the request data is invalid.
    
    Attributes:
        request (Request): The incoming request.
    """
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderListCreateView(APIView):
    """
    API view to retrieve and create Order instances.

    This view provides the following functionalities:
    
    - **GET**: Retrieve a list of all orders.
        - Response: A JSON array containing order details.
        - Status Code: 200 OK if successful.
        
    - **POST**: Create a new order instance.
        - Request Body: A JSON object containing order details.
        - Response: The created order's details.
        - Status Codes:
            - 201 Created: If the order is successfully created.
            - 400 Bad Request: If the request data is invalid.
    
    Attributes:
        request (Request): The incoming request.
    """
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderUpdateView(APIView):
    """
    API view to update an existing Order instance.

    This view allows the following functionality:

    - **PUT**: Update an existing order instance based on the provided primary key (pk).
        - Request Body: A JSON object containing the fields to be updated. Partial updates are allowed.
        - URL Parameter:
            - `pk`: The primary key of the order to be updated.
        - Response: The updated order's details.
        - Status Codes:
            - 200 OK: If the order is successfully updated.
            - 404 Not Found: If the order with the given primary key does not exist.
            - 400 Bad Request: If the request data is invalid.

    Attributes:
        request (Request): The incoming request.
        pk (int): The primary key of the order instance to update.
    """
    def put(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderFilterByProductView(APIView):
    """
    API view to filter orders by associated product names.

    This view provides the following functionality:

    - **GET**: Retrieve a list of orders filtered by product names.
        - Query Parameter:
            - `products`: A comma-separated string of product names to filter the orders.
        - Response: A JSON array containing the details of orders that include the specified products.
        - Status Code: 200 OK if successful.

    If no product names are provided, all orders will be returned.

    Attributes:
        request (Request): The incoming request.
        args (tuple): Positional arguments passed to the view.
        kwargs (dict): Keyword arguments passed to the view.
    """
    def get(self, request, *args, **kwargs):
        queryset = Order.objects.all()
        product_names = request.query_params.get('products', None)
        if product_names:
            product_names_list = product_names.split(',')
            product_ids = Product.objects.filter(product_name__in=product_names_list).values_list('product_id', flat=True)
            queryset = queryset.filter(order_items__product_id__in=product_ids).distinct()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderFilterByCustomerView(APIView):
    """
    API view to filter orders by associated customer name.

    This view provides the following functionality:

    - **GET**: Retrieve a list of orders filtered by customer name.
        - Query Parameter:
            - `customer_name`: The name of the customer to filter the orders.
        - Response: A JSON array containing the details of orders associated with the specified customer.
        - Status Codes:
            - 200 OK: If orders are successfully retrieved.
            - 404 Not Found: If no customer with the given name exists.

    If no customer name is provided, all orders will be returned.

    Attributes:
        request (Request): The incoming request.
        args (tuple): Positional arguments passed to the view.
        kwargs (dict): Keyword arguments passed to the view.
    """
    def get(self, request, *args, **kwargs):
        queryset = Order.objects.all()
        customer_name = request.query_params.get('customer_name', None)
        print(f"Received customer_name: {customer_name}")
        if customer_name:
            try:
                customer = Customer.objects.get(customer_name__iexact=customer_name)
                print(f"Found customer: {customer}")
                queryset = queryset.filter(customer_id=customer).distinct()
            except Customer.DoesNotExist:
                return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)