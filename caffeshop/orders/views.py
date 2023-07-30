from django.shortcuts import render
from .models import Order, Order_detail
from menu.models import Product, Category, ParentCategory
import json
# Create your views here.

def cart(request):
    orders = request.COOKIES.get('orders', '{}')
    orders = orders.replace("\'", "\"")
    orders = json.loads(orders)
    print('orders: ',orders)
    print('type orders: ',type(orders))

    order_items = [(Product.objects.get(id=product_id), quantity, Product.objects.get(id=product_id).price_per_item  * quantity) for product_id, quantity in orders.items()]
    if request.method == 'GET':
        return render(request, 'orders/cart.html', {'order_items':order_items})