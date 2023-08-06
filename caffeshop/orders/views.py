from django.contrib import messages
from django.shortcuts import render, redirect
from menu.models import Product
from .models import Order, Order_detail
from .forms import OrderForm
from utils import check_availability
import re


# Create your views here.

def cart(request):
    orders = request.COOKIES.get('orders', '{}')
    orders = eval(orders)
    updated_orders = orders.copy()
    form = OrderForm()
    order_items = []
    for product_id, quantity in orders.items():
        qs = Product.objects.filter(id=product_id)
        if qs.exists():
            obj = qs.get(id=product_id)
            message, obj = check_availability(obj)
            if obj:
                tp = obj.price * int(quantity)
                order_items.append((obj, quantity, tp))
            else:
                updated_orders.pop(product_id)
                messages.error(request, message)
        else:
            messages.error(request, f'Product {obj.name} is not available!!')
            updated_orders.pop(product_id)
    order_total_price = sum(map(lambda item: int(item[2]), order_items))
    context = {'order_items': order_items,
               'order_total_price': order_total_price,
               'form': form}
    request.COOKIES['number_of_order_items'] = sum([int(order_qnt) for order_qnt in updated_orders.values()])
    response = render(request, 'orders/cart.html', context=context)
    response.set_cookie('orders', updated_orders)
    if request.method == 'GET':
        return response
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if request.POST.get('table_number'):
            if form.is_valid():
                phone = form.cleaned_data["phone"]
                pre_order = {"phone": phone, "table_number": request.POST.get('table_number')}
                request.session['pre_order'] = pre_order
                request.session.modify = True
                return redirect('orders:create_order')
        else:
            if form["phone"].value() and re.match(r"^09\d{9}$", str(form["phone"].value())):
                phone = form["phone"].value()
                pre_order = {"phone": phone}
                request.session['pre_order'] = pre_order
                request.session.modify = True
                return redirect('orders:create_order')
            else:
                messages.error(request, 'Your phone number is not valid!!')
                return redirect('orders:cart')


def update_or_remove(request):
    if request.method == 'POST':
        orders = request.COOKIES.get('orders', '{}')
        orders = eval(orders)
        updated_orders = orders.copy()
        if request.POST.get('update'):
            updated_orders[request.POST.get('product')] = request.POST.get('quantity')
        if request.POST.get('remove'):
            updated_orders.pop(request.POST.get('product'))
        response = redirect('orders:cart')
        response.set_cookie('orders', updated_orders)
        response.set_cookie('number_of_order_items', sum([int(order_qnt) for order_qnt in updated_orders.values()]))
        return response


def create_order(request):
    pre_order = request.session['pre_order']
    customer_order = Order.objects.create(phone_number=pre_order['phone'],
                                          table_number=int(pre_order['table_number']))

    orders = request.COOKIES.get('orders', '{}')
    orders = eval(orders)
    for product_id, quantity in orders.items():
        product = Product.objects.get(id=product_id)

        Order_detail.objects.create(order=customer_order, product=product, quantity=int(quantity),
                                    price=product.price)

    customer_order.save()

    messages.success(request, "Order has been created successfully.")
    res = redirect("home")
    res.delete_cookie('orders')
    res.delete_cookie('number_of_order_items')

    request.session['order_history'] = customer_order.id

    del request.session['pre_order']
    return res


def order_history(request):
    if request.method == "GET":
        customer_order_id = request.session.get('order_history')
        if customer_order_id:
            order = Order.objects.get(id=customer_order_id)
            order_item = Order_detail.objects.filter(order=order.id)

            context = {"last_order": order, "order_item": order_item}
            return render(request, "orders/order_history.html", context=context)
        else:
            messages.error(request, "You Don't have any order yet.")
            return redirect("home")