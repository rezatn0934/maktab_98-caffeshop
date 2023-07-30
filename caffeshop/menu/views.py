from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404 , HttpResponse, HttpResponseRedirect                      
from .models import Product, Category, ParentCategory
from django.db.models import Q
import datetime
import json
# Create your views here.


def menu(request):
    categories =   ParentCategory.objects.all()
    products = Product.objects.all()
    orders = request.COOKIES.get('orders', '{}')
    orders = orders.replace("\'", "\"")
    orders = json.loads(orders)
    context = {'categories': categories, 'products': products}
    html = render(request, 'menu\menu.html', context)
    html.set_cookie('number_of_order_items', sum([int(order_qnt) for order_qnt in orders.values()]))
    if request.method == 'GET':
        return html
    elif request.method == 'POST':
        product = request.POST.get('product')
        number_of_product = int(request.POST.get('quantity'))
        html = HttpResponseRedirect(request.path)
        if request.COOKIES.get('orders'):
            if orders.get(product):
                orders[product] += number_of_product
                message = "Order updated"
            else:
                orders[product] = number_of_product 
                message = "Order added"
            html.set_cookie('orders', orders)
            html.set_cookie('message', message)
        else:
            orders = {product: number_of_product}
            html.set_cookie('orders', orders)
            message = "you created a shopping cart"
            html.set_cookie('message', message)
        html.set_cookie( 'number_of_order_items', sum([int(order_qnt) for order_qnt in orders.values()]))
        return html

def product(request, name):
    pro = Product.objects.get(name = name)
    return render(request, 'menu/product.html', {'product':pro})