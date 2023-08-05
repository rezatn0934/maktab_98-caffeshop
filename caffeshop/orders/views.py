from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from menu.models import Product
from home.models import BackgroundImage
from .models import Order, Order_detail
from .forms import ReserveForm
from utils import send_otp_code, check_availability
import datetime
import json
import re


# Create your views here.

def cart(request):
    orders = request.COOKIES.get('orders', '{}')
    orders = eval(orders)
    updated_orders = orders.copy()
    form = ReserveForm()
    order_items = []
    for product_id, quantity in orders.items():
        qs = Product.objects.filter(id=product_id)
        if qs.exists():
            obj = qs.get(id=product_id)
            message, obj = check_availability(obj, quantity)
            if obj:
                tp = obj.price_per_item * int(quantity)
                order_items.append((obj, quantity, tp))
            else:
                updated_orders.pop(product_id)
                messages.error(request, message)
        else:
            messages.error(request, f'Product {obj.name} is not available!!')
            updated_orders.pop(product_id)
    order_total_price = sum(map(lambda item: int(item[2]), order_items))
    background_image = BackgroundImage.objects.get(is_active=True)
    context = {'order_items': order_items,
               'order_total_price': order_total_price,
               'background_image': background_image,
               'form': form}
    request.COOKIES['number_of_order_items'] = sum([int(order_qnt) for order_qnt in updated_orders.values()])
    response = render(request, 'orders/cart.html', context=context)
    response.set_cookie('orders', updated_orders)
    if request.method == 'GET':
        return response
    if request.method == 'POST':
        form = ReserveForm(request.POST)
        date = " ".join([request.POST.get('reserve_date'), request.POST.get('reserve_time')])
        reserve_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
        if date:
            if request.POST.get('table_number'):
                if form.is_valid():
                    phone = form.cleaned_data["phone"]
                    pre_order = {"phone": phone, "table_number": request.POST.get('table_number'),
                                 "reserve_date": str(reserve_date), "delivery": ('in', 'indoor')}
                    request.session['pre_order'] = pre_order
                    request.session.modify = True
                    return redirect('orders:create_order')
            else:
                if form["phone"].value() and re.match(r"^09\d{9}$", str(form["phone"].value())):
                    phone = form["phone"].value()
                    pre_order = {"phone": phone, "reserve_date": str(reserve_date), "delivery": ('out', 'outdoor')}
                    request.session['pre_order'] = pre_order
                    request.session.modify = True
                    return redirect('orders:create_order')
                else:
                    messages.error(request, 'Your phone number is not valid!!')
                    return redirect('orders:cart')
        else:
            messages.error(request, "You didn't choose a date!!")
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
    if request.method == 'POST':
        pre_order = request.session['pre_order']
        if pre_order['delivery'][0] == 'in':
            customer_order = Order.objects.create(phone_number=pre_order['phone'],
                                                    table_number=int(pre_order['table_number']),
                                                    delivery=tuple(pre_order['delivery'])[0],
                                                    reservation_date=datetime.datetime.fromisoformat(
                                                        pre_order['reserve_date']))

        elif pre_order['delivery'][0] == 'out':
            customer_order = Order.objects.create(phone_number=pre_order['phone'],
                                                    delivery=tuple(pre_order['delivery'])[0],
                                                    reservation_date=datetime.datetime.fromisoformat(
                                                        pre_order['reserve_date']))

        orders = request.COOKIES.get('orders', '{}')
        orders = eval(orders)
        total_order_price = 0
        available_pro = []
        order_details_list = []
        for product_id, quantity in orders.items():
            qs = Product.objects.filter(id=product_id)
            if qs.exists():
                obj = qs.get(id=product_id)
                result = check_availability(obj, quantity)
                if result[1]:
                    tp = obj.price_per_item * int(quantity)
                    total_order_price += tp
                    available_pro.append([customer_order, obj, int(quantity), obj.price_per_item, tp])
                    order_details_list.append([obj.name, int(quantity),
                                                obj.price_per_item, tp,
                                                str(customer_order.date)])

                else:
                    messages.error(request, result[0])
                    customer_order.delete()
                    return redirect("orders:cart")
            else:
                messages.error(request, f'Product {obj.name} is not available!!')
                customer_order.delete()
                return redirect("orders:cart")
        [Order_detail.objects.create(order=res[0], product=res[1], quantity=res[2],
            price=res[3], total_price=res[4]) for res in available_pro]
        customer_order.total_price = total_order_price
        customer_order.save()

        messages.success(request, "Order has been created successfully.")
        res = redirect("home")
        res.delete_cookie('orders')
        res.delete_cookie('number_of_order_items')

        if request.session.get('order_history'):
            request.session['order_history'].append(order_details_list)
            request.session['order_info'].append([customer_order.id, total_order_price])
        else:
            request.session['order_history'] = [order_details_list]
            info = [customer_order.id, total_order_price]
            request.session['order_info'] = [info]

        request.session.modify = True
        del request.session['pre_order']
        return res


def order_history(request):
    if request.method == "GET":
        order_list = request.session['order_history']
        order_info = request.session['order_info']
        order_info = order_info[-1]
        last_order = order_list[-1]
        pre_order = order_list[:-1]
        context = {"last_order": last_order, "pre_order": pre_order, 'last_order_info': order_info}
        return render(request, "orders/order_history.html", context=context)
