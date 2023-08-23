from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone

from menu.models import Product
from .models import Order, Order_detail, Table
from .forms import OrderForm
from utils import check_availability
from .cart import just_available_product, orders_from_cookie

import datetime
import json



class CartView(View):

    def get(self, request):
        form = OrderForm()
        if user_phone := request.session.get('user_phone'):
            form = OrderForm(initial={'phone_number': user_phone})
        context = {'form': form}
        response = render(request, 'orders/cart.html', context=context)
        return response

    def post(self, request):
        form = OrderForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone_number"]
            table = form.cleaned_data["table_number"]
            if table:
                pre_order = {"phone": phone, "table_number": table.Table_number}
            else:
                pre_order = {"phone": phone, "table_number": None}
            request.session['pre_order'] = pre_order
            request.session['user_phone'] = phone
            request.session.modify = True
            return redirect('orders:create_order')
        else:
            messages.error(request, 'Your phone number is not valid!!')
            return redirect('orders:cart')
        

def create_order(request):
    pre_order = request.session['pre_order']
    if pre_order['table_number']:
        table = Table.objects.get(Table_number=pre_order['table_number'])
    else:
        table = None
    customer_order = Order.objects.create(phone_number=pre_order['phone'],
                                          table_number=table)
    orders = orders_from_cookie(request)
    order_items, updated_orders = just_available_product(request, orders)
    if orders.items() != updated_orders.items():
        return redirect('orders:cart')
    for product, quantity in order_items:
        Order_detail.objects.create(order=customer_order, product=product, quantity=quantity,
                                    price=product.price)
    customer_order.save()
    messages.success(request, "Order has been created successfully.")
    response = redirect("orders:order_history")
    response.delete_cookie('orders')
    response.delete_cookie('number_of_order_items')

    if order_history_session := request.session.get('order_history'):
        order_history_session.append(customer_order.id)
    else:
        request.session['order_history'] = [customer_order.id]

    request.session.modified = True

    del request.session['pre_order']
    return response


def order_history(request):
    if request.method == "GET":

        if customer_order_id := request.session.get('order_history'):
            orders = Order.objects.filter(id__in=customer_order_id).order_by('-order_date')
            context = {"orders": orders}
            return render(request, "orders/order_history.html", context=context)

        else:
            message = "You Don't have any order yet."
            return render(request, "orders/order_history.html", context={"message": message})

def cancel_order_by_customer(request, pk):
    order = Order.objects.filter(id=pk)
    if order:
        order = order.get(id=pk)
        order.status = 'C'
        order.save()
        return redirect('orders:order_history')
