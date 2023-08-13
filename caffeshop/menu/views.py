from django.shortcuts import render, HttpResponseRedirect
from django.db.models import Q
from django.views import View
from .models import Product, Category


# Create your views here.

class Menu(View):

    def get(self, request):
        categories = Category.objects.all()
        products = Product.objects.all()
        print(request.COOKIES.get('orders', '{}'))
        # orders = eval(request.COOKIES.get('orders', '{}'))
        context = {'categories': categories, 'products': products}
        response = render(request, 'menu/menu.html', context)
        # response.set_cookie('number_of_order_items', sum([int(order_qnt) for order_qnt in orders.values()]))
        return response

    def post(self, request):
        orders = eval(request.COOKIES.get('orders', '{}'))
        product = request.POST.get('product')
        number_of_product = int(request.POST.get('quantity'))
        response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/menu/'))
        if request.COOKIES.get('orders'):
            if orders.get(product):
                orders[product] += number_of_product
                message = "Order updated"
            else:
                orders[product] = number_of_product
                message = "Order added"
            response.set_cookie('orders', orders)
            response.set_cookie('message', message)
        else:
            orders = {product: number_of_product}
            response.set_cookie('orders', orders)
            message = "you created a shopping cart"
            response.set_cookie('message', message)
        response.set_cookie('number_of_order_items', sum([int(order_qnt) for order_qnt in orders.values()]))
        return response


def product(request, name):
    product = Product.objects.get(name=name)
    return render(request, 'menu/product.html', {'product': product})


def search_product_view(request):
    if request.method == 'GET':
        search_query = request.GET.get('search')
        search_result = None
        message = None
        if search_query:
            search_result = Product.objects.filter(Q(name__icontains=search_query) |
                                                   Q(description__icontains=search_query) |
                                                   Q(category__name__icontains=search_query)).distinct()
            if not search_result.exists():
                message = f"Nothing was found for {search_query}"

        context = {'search_result': search_result, "message": message}
        return render(request, 'menu/search.html', context=context)

