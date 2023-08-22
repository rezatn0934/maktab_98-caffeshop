from orders.models import Order
from django.db.models import Q
from datetime import datetime, timedelta
def chart_access_check(user):
    return user.groups.filter(name__in=['Managers', 'Supervisiors', 'Cashier'])



class FilterMixin:


    def check_sort(self, request):
        sort = request.GET.get('sort', 'title')
        orderp = request.GET.get('orderp')
        if sort == 'id' or sort == 'phone_number' or sort == 'order_date' or \
                sort == 'table_number' or sort == 'status' or sort == 'payment':
            sort_param = sort if orderp == 'asc' else '-' + sort
            orders = Order.objects.all().order_by(sort_param)
        else:
            orders = Order.objects.all().order_by('-order_date')
        context = {
            'orderp': 'desc' if orderp == 'asc' else 'asc',
            'sort': sort,
        }
        return (context, orders)
