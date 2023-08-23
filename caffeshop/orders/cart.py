from .models import Product , Category
from utils import check_availability
from django.contrib import messages

import json


def orders_from_cookie(request):
    orders = request.COOKIES.get('orders', '{}')
    orders = str(orders.replace('\'','\"'))
    return json.loads(orders)


def get_order_info(request, orders):
    updated_orders = orders.copy()
    order_items = []
    for product_id, info in orders.items():
        order_items.append((product_id, info.get('name'), info.get('quantity'),
                            info.get('price'), (int(info.get('quantity')) * int(info.get('price'))), info.get('image_url'), info.get('detail_url')))

    request.COOKIES['number_of_order_items'] = sum([int(order_info['quantity']) for order_info in updated_orders.values()])    
    return order_items, updated_orders


def just_available_product(request, orders):
    updated_orders = orders.copy()
    order_items = []
    for product_id, info in orders.items():
        qs = Product.objects.filter(id=product_id)
        if qs.exists():
            obj = qs.get(id=product_id)
            message, obj = check_availability(obj)
            if obj:
                order_items.append((obj, info.get('quantity')))
            else:
                updated_orders.pop(product_id)
                messages.error(request, message)
        else:
            messages.error(request, f'Product {product_id} is not available!!')
            updated_orders.pop(product_id)
    request.COOKIES['number_of_order_items'] = sum([int(order_info['quantity']) for order_info in updated_orders.values()])    
    return order_items, updated_orders