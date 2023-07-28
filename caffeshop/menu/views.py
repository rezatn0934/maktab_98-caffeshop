from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404 , HttpResponse                        
from .models import Product, Category
from django.db.models import Q
import datetime
import json
# Create your views here.


def menu(request):
    categories = get_list_or_404(Category)
    products = get_list_or_404(Product)
    orders = request.COOKIES.get('orders', '{}')
    orders = orders.replace("\'", "\"")
    orders = json.loads(orders)
    context = {'categories': categories, 'products': products, 'number_of_order_items': sum([int(order_qnt) for order_qnt in orders.values()])}
    html = render(request, 'menu\menu.html', context)
    html.set_cookie('number_of_order_items', sum([int(order_qnt) for order_qnt in orders.values()]))
    if request.method == 'GET':
        return html
    