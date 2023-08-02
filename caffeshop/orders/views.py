from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from menu.models import Product
from home.models import BackgroundImage
from .models import Order, Order_detail
from .forms import ReserveForm
from utils import send_otp_code
import datetime
import json
import re


# Create your views here.

def cart(request):
    orders = request.COOKIES.get('orders', '{}')
    orders = orders.replace("\'", "\"")
    orders = json.loads(orders)
    updated_orders = orders.copy()
    form = ReserveForm()
    order_items = []
    for product_id, quantity in orders.items():
        qs = Product.objects.filter(id=product_id)
        if qs.exists():
            obj = qs.get(id=product_id)
            tp = obj.price_per_item * int(quantity)
            order_items.append((obj, quantity, tp))
        else:
            updated_orders.pop(product_id)
    order_total_price = sum(map(lambda item: int(item[2]), order_items))
    background_image = BackgroundImage.objects.get(is_active=True)
    context = {'order_items': order_items,
               'order_total_price': order_total_price,
               'background_image': background_image,
               'form': form}
    response = render(request, 'orders/cart.html', context=context)
    response.set_cookie('orders', updated_orders)
    response.set_cookie('number_of_order_items', sum([int(order_qnt) for order_qnt in updated_orders.values()]))
    if request.method == 'GET':
        return response
    if request.method == 'POST':
        form = ReserveForm(request.POST)
        date = " ".join([request.POST.get('reserve_date'), request.POST.get('reserve_time')])
        reserve_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
        if date:
            context['reserve_validation'] = True
            if request.POST.get('table_number'):
                if form.is_valid():
                    phone = form.cleaned_data["phone"]
                    pre_order = {"phone": phone, "table_number": request.POST.get('table_number'),
                                 "reserve_date": str(reserve_date), "delivery": ('in', 'indoor')}
                    request.session['pre_order'] = pre_order
                    request.session.modify = True
                    send_otp_code(request, phone)
                    return render(request, 'orders/cart.html', context)
            else:
                if form["phone"].value() and re.match(r"^09\d{9}$", str(form["phone"].value())):
                    phone = form["phone"].value()
                    pre_order = {"phone": phone, "reserve_date": str(reserve_date), "delivery": ('out', 'outdoor')}
                    request.session['pre_order'] = pre_order
                    request.session.modify = True
                    send_otp_code(request, phone)

                    return render(request, 'orders/cart.html', context)
                else:
                    messages.error(request, 'Your phone number is not valid!!')
                    return redirect('orders:cart')
        else:
            messages.error(request, "You didn't choose a date!!")
            return redirect('orders:cart')


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


def create_order(request):
    if request.method == 'POST':
        user_verfication_input = request.POST.get('verfication_user_code')
        otp_code = request.session["otp_code"]
        otp_valid_date = request.session["otp_valid_date"]
        valid_until = datetime.datetime.fromisoformat(otp_valid_date)
        if timezone.now() < valid_until:
            if otp_code == user_verfication_input:
                if request.session['pre_order']['delivery'][0] == 'in':
                    customer_order = Order.objects.create(phone_number=request.session['pre_order']['phone'],
                                                          table_number=int(
                                                              request.session['pre_order']['table_number']),
                                                          delivery=tuple(request.session['pre_order']['delivery'])[0],
                                                          reservation_date=datetime.datetime.fromisoformat(
                                                              request.session['pre_order']['reserve_date']))

                elif request.session['pre_order']['delivery'][0] == 'out':
                    customer_order = Order.objects.create(phone_number=request.session['pre_order']['phone'],
                                                          delivery=tuple(request.session['pre_order']['delivery'])[0],
                                                          reservation_date=datetime.datetime.fromisoformat(
                                                              request.session['pre_order']['reserve_date']))

                orders = request.COOKIES.get('orders', '{}')
                orders = orders.replace("\'", "\"")
                orders = json.loads(orders)
                updated_orders = orders.copy()
                total_order_price = 0
                for product_id, quantity in orders.items():
                    qs = Product.objects.filter(id=product_id)
                    if qs.exists():
                        obj = qs.get(id=product_id)
                        tp = obj.price_per_item * int(quantity)
                        total_order_price += tp
                        Order_detail.objects.create(
                            order=customer_order,
                            product=obj,
                            quantity=int(quantity),
                            price=obj.price_per_item,
                            total_price=tp)
                    else:
                        updated_orders.pop(product_id)
                customer_order.total_price = total_order_price
                customer_order.save()

                messages.success(request, "Order has been created successfully.")
                res = redirect("home")
                res.delete_cookie('orders')
                res.delete_cookie('number_of_order_items')

                del request.session["otp_code"]
                del request.session["otp_valid_date"]
                return res
            else:
                messages.error(request, "Your verification code is invalid")
                return redirect("orders:cart")
        else:
            messages.error(request, "Code has been expired")
            return redirect("orders:cart")
