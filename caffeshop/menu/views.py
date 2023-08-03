from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404 , HttpResponse, HttpResponseRedirect                      
from .models import Product, Category, ParentCategory
from django.db.models import Q
import datetime
import json
from . models import Product
# Create your views here.


def menu(request):
    categories = ParentCategory.objects.all()
    products = Product.objects.all()
    orders = request.COOKIES.get('orders', '{}')
    orders = orders.replace("\'", "\"")
    orders = json.loads(orders)
    context = {'categories': categories, 'products': products}
    html = render(request, 'menu/menu.html', context)
    html.set_cookie('number_of_order_items', sum([int(order_qnt) for order_qnt in orders.values()]))
    if request.method == 'GET':
        return html
    elif request.method == 'POST':
        product = request.POST.get('product')
        number_of_product = int(request.POST.get('quantity'))
        html = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/menu/'))
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


def search_product_view(request):
    search_query = request.GET.get('search')
    checkbox = request.GET.getlist('checkbox')
    if request.method == 'GET':
        if search_query:
            query_list = []

            if 'a' in checkbox:
                query_list.append(Q(name__icontains=search_query))
            if 'b' in checkbox:
                query_list.append(Q(description__icontains=search_query))
            if 'c' in checkbox:
                query_list.append(Q(category__name__icontains=search_query))

            if not query_list:
                query_list.append(Q(name__icontains=search_query) |
                                  Q(description__icontains=search_query) |
                                  Q(category__name__icontains=search_query))

            products = Product.objects.filter(*query_list).distinct()
        else:
            products = None
        return render(request, 'menu/search.html', {'search_query': search_query, 'products': products})
    else:
        return redirect(request.path)

