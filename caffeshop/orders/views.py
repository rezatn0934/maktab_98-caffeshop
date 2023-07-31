from django.shortcuts import render , HttpResponse , HttpResponseRedirect , redirect
from .models import Order, Order_detail
from menu.models import Product, Category, ParentCategory
from django.urls import reverse
import json
# Create your views here.

def cart1(request):
    orders = request.COOKIES.get('orders', '{}')
    orders = orders.replace("\'", "\"")
    orders = json.loads(orders)
    updated_orders = orders.copy()
    order_items = []
    for product_id, quantity in orders.items():
        qs = Product.objects.filter(id=product_id)
        if qs.exists():
            obj = qs.get(id=product_id)
            tp =  obj.price_per_item * int(quantity)        
            order_items.append((obj , quantity, tp))
        else :
            updated_orders.pop(product_id)
    order_total_price = sum(map(lambda item: int(item[2]), order_items))
    response = render(request, 'orders/cart.html', {'order_items':order_items, 'order_total_price': order_total_price})
    response.set_cookie('orders', updated_orders)
    response.set_cookie('number_of_order_items', sum([int(order_qnt) for order_qnt in updated_orders.values()]))
    if request.method == 'GET':
        return response

    
def update_or_remove(request):
    if request.method == 'POST':
        orders = request.COOKIES.get('orders', '{}')
        orders = orders.replace("\'", "\"")
        orders = json.loads(orders)
        updated_orders = orders.copy()
        if request.POST.get('update'):
            updated_orders[request.POST.get('product')] = request.POST.get('quantity')
        if request.POST.get('remove'):
            updated_orders.pop(request.POST.get('product'))
        response = redirect('orders:cart')
        response.set_cookie('orders', updated_orders)
        response.set_cookie('number_of_order_items', sum([int(order_qnt) for order_qnt in updated_orders.values()]))
        return response