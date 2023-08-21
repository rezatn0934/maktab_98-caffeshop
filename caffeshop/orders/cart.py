from .models import Product , Category
from utils import check_availability
from django.contrib import messages

import json


def orders_from_cookie(request):
    orders = request.COOKIES.get('orders', '{}')
    orders = str(orders.replace('\'','\"'))
    return json.loads(orders)


def just_available_product(request, orders):
    updated_orders = orders.copy()
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
    request.COOKIES['number_of_order_items'] = sum([int(order_qnt) for order_qnt in updated_orders.values()])    
    return order_items, updated_orders