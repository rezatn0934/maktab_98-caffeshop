from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, F, Sum, Func, Value, CharField, Count
from django.db.models.functions import TruncMonth, TruncYear, TruncHour, ExtractHour

from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views import View

from .authentication import PhoneAuthBackend
from .form import StaffLoginForm, VerifyCodeForm, OrderDetailUpdateForm
from orders.models import Order, Order_detail
from utils import send_otp_code, check_is_authenticated
from menu.models import Product

import datetime
import time


# Create your views here.


class StaffLogin(View):
    message = None
    form = StaffLoginForm
    html_temp = "login.html"

    def get(self, request):
        if response := check_is_authenticated(request):
            return response
        context = {"message": self.message, "form": self.form()}
        return render(request, self.html_temp, context=context)

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"]
            request.session["phone"] = phone
            return redirect("verify")
        else:
            message = "Wrong input, Phone number Should Start 11 digits Like 09*********"

        context = {"message": message, "form": self.form()}
        return render(request, self.html_temp, context=context)


class Verify(View):
    message = None
    form = VerifyCodeForm
    html_temp = "verify.html"

    def get(self, request):
        if response := check_is_authenticated(request):
            return response
        if request.session.get("phone") is None:
            return redirect("login")

        message = "6-digit code was sent for you, you only have 60 seconds"
        send_otp_code(request, request.session.get("phone"))
        context = {"message": message, "form": self.form()}
        return render(request, self.html_temp, context=context)

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user_input_otp = cd["otp_code"]
            phone = request.session["phone"]
            try:
                user = PhoneAuthBackend().authenticate(request, phone=phone,
                                                       user_input_otp=user_input_otp)
                login(request, user, backend='accounts.authentication.PhoneAuthBackend')
                del request.session["otp_code"]
                del request.session["otp_valid_date"]
                messages.success(request, 'You have been logged in successfully')
                return redirect("dashboard")
            except Exception as e:
                message = e
                if message == "Login First":
                    return redirect("login")
        else:
            message = "Wrong Input"

        context = {"message": message, "form": form}
        return render(request, self.html_temp, context=context)


class Dashboard(View):

    @method_decorator(login_required)
    def get(self, request):
        return render(request, "dashboard.html")


class Orders(View):

    @method_decorator(login_required)
    def get(self, request):
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

        if 'search' in request.GET:
            filter_item = request.GET.get('filter1')
            field = request.GET.get('flexRadioDefault')

            if field == 'table_number':
                if filter_item:
                    orders = orders.filter(Q(table_number__Table_number__icontains=filter_item) |
                                           Q(table_number__name__icontains=filter_item))
                else:
                    orders = orders.filter(table_number=None)
                context['flexRadioDefault'] = field
                context['filter1'] = filter_item
                context['search'] = 'search'
            elif field == 'phone_number':
                orders = orders.filter(phone_number__icontains=filter_item)
                context['flexRadioDefault'] = field
                context['filter1'] = filter_item
                context['search'] = 'search'

        if 'filter' in request.GET:
            first_date = request.GET.get('first_date')
            if first_date:
                second_date = request.GET.get('second_date')
                if not second_date:
                    second_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
                orders = orders.filter(order_date__range=(first_date, second_date))
                context['filter'] = 'filter'
                context['first_date'] = first_date
                context['second_date'] = second_date

        if 'paid' in request.GET:
            paid_order = Order.objects.filter(id=request.GET['paid'])

            if paid_order:
                order = paid_order.get(id=request.GET['paid'])
                order.payment = 'P'
                order.save()
        paginator = Paginator(orders, 5)
        page_number = request.GET.get('page', 1)
        orders = paginator.get_page(page_number)
        context['orders'] = orders
        context['page'] = page_number
        return render(request, 'orders_list.html', context)


class OrderDetailView(View):

    @method_decorator(login_required)
    def get(self, request, pk):
        order = Order.objects.filter(id=pk)
        products = Product.objects.filter(is_active=True)
        if order:
            order = order.get(id=pk)
            order_details = Order_detail.objects.filter(order=pk)
            context = {
                'order': order,
                'order_details': order_details,
                'products': products
            }
            return render(request, 'order_detail.html', context)
        else:
            messages.error(request, f'Order {pk} not found')
            return redirect('order_list')

    @method_decorator(login_required)
    def post(self, request, pk):
        order_detail = Order_detail.objects.get(id=pk)
        if request.POST.get('s_product') and request.POST.get('quantity'):
            product = Product.objects.get(id=request.POST.get('s_product'))
            order_detail.product = product
            order_detail.price = product.price
            order_detail.quantity = request.POST.get('quantity')
            order_detail.save()
            messages.success(request, 'Order item has been successfully updated.')
            return redirect('order_detail', order_detail.order.id)
        else:
            messages.error(request, 'Form input is not valid')
            return redirect('order_detail', order_detail.order.id)


@login_required
def confirm_order(request, pk):
    if request.method == 'GET':
        order = Order.objects.filter(id=pk)
        if order:
            order = order.get(id=pk)
            order.status = 'A'
            order.save()
            messages.success(request, f'Order {pk} has been successfully Approved.')
            return redirect('order_list')
        else:
            messages.error(request, f'Order {pk} not found')
            return redirect('order_detail', pk)


@login_required
def cancel_order(request, pk):
    if request.method == 'GET':
        order = Order.objects.filter(id=pk)
        if order:
            order = order.get(id=pk)
            order.status = 'C'
            order.save()
            messages.warning(request, f'Order {pk} has been canceled.')
            return redirect('order_list')
        else:
            messages.error(request, f'Order {pk} not found')
            return redirect('order_detail', pk)


@login_required
def delete_order_detail(request, pk):
    if request.method == 'GET':
        order_detail = Order_detail.objects.filter(id=pk)
        if order_detail:
            order_detail = order_detail.get(id=pk)
            order = order_detail.order
            order_detail.delete()
            messages.warning(request, f'Order item {pk} has been canceled!')
            return redirect('order_detail', order.id)
        else:
            messages.error(request, f'Order items {pk} not found')
            return redirect('order_list')


class CreateOrderItem(View):
    @method_decorator(login_required)
    def post(self, request, pk):
        if request.POST.get('s_product') and request.POST.get('quantity'):
            product = Product.objects.get(id=request.POST.get('s_product'))
            quantity = request.POST.get('quantity')
            order = Order.objects.get(id=pk)
            order_detail = Order_detail.objects.create(order=order, product=product, quantity=quantity,
                                                       price=product.price)
            messages.success(request, f'Order item {order_detail.id} has benn successfully added to Order {pk}')
        else:
            messages.error(request, "You didn't provide valid inputs")

        return redirect('order_detail', pk)


def most_popular(request):
    if 'filter' in request.GET:
        first_date = request.GET.get('first_date')
        second_date = request.GET.get('second_date')
        limit = int(request.GET.get('quantity'))
        query_set = Order_detail.objects.all().annotate(date=F('order__order_date')).filter(
            date__range=[first_date, second_date]).values('product').annotate(order_count=Count('id')).annotate(
            name=F('product__name')).order_by(
            '-order_count')[:limit]
    else:
        limit = 5
        query_set = Product.objects.all().annotate(
            order_count=Count('order_detail')
        ).order_by('-order_count')[:limit]

    return render(request, 'analytics/most_popular.html', {'query_set': query_set})


def total_sales(request):
    total_sale = Order.objects.aggregate(
        total_sale=Sum(
            F('order_detail__quantity') *
            F('order_detail__price')
        )
    )
    return render(request, 'result.html', {'query_set': total_sale})


def peak_business_hour(request):
    lst2 = None
    first_date2 = None
    lst1 = [0 for _ in range(24)]
    if 'filter' in request.GET:
        first_date1 = request.GET.get('first_date')
        second_date1 = (datetime.datetime.strptime(first_date1, '%Y-%m-%d') + timezone.timedelta(
            days=1)).strftime('%Y-%m-%d')

        if first_date2 := request.GET.get('second_date'):

            lst2 = [0 for _ in range(24)]
            second_date2 = (datetime.datetime.strptime(first_date2, '%Y-%m-%d') + timezone.timedelta(
                days=1)).strftime('%Y-%m-%d')
            query_set2 = Order.objects.filter(order_date__range=[first_date2, second_date2]).annotate(
                hour=ExtractHour('order_date')).values('hour').annotate(order_count=Count('id')).order_by('hour')
            for query in query_set2:
                index = int(query['hour'])
                lst2[index] = query['order_count']

    else:
        first_date1 = timezone.now().date()
        second_date1 = timezone.now()

    query_set1 = Order.objects.filter(order_date__range=[first_date1, second_date1]).annotate(
        hour=ExtractHour('order_date')).values('hour').annotate(order_count=Count('id')).order_by('hour')
    for query in query_set1:
        index = int(query['hour'])
        lst1[index] = query['order_count']

    context = {'lst1': lst1, 'lst2': lst2, "first_date1": first_date1, "first_date2": first_date2}
    return render(request, 'analytics/peak_business_hour.html', context=context)


def top_selling(request):
    query_set = Product.objects.annotate(
        total=Sum(
            F('order_detail__quantity') *
            F('order_detail__price')
        )).filter(Q(total__isnull=False)).order_by('-total')
    return render(request, 'result.html', {'query_set': query_set})


def hourly_sales(request):
    if 'filter' in request.GET:
        first_date = request.GET.get('first_date').strptime('%Y-%m-%d')
        second_date = first_date.date + datetime.timedelta(days=1)
    else:
        first_date = datetime.datetime.now().date()
        second_date = datetime.datetime.now()
    query_set = Order.objects.filter(order_date__range=[first_date, second_date]) \
        .annotate(
        hour=TruncHour('order_date')).values('hour') \
        .annotate(
        total_sale=Sum(
            F('order_detail__quantity') *
            F('order_detail__price'))).order_by('-hour')
    return render(request, 'result.html', {'query_set': query_set})


def daily_sales(request):
    if 'filter' in request.GET:
        first_date = request.GET.get('first_date')
        second_date = request.GET.get('second_date')
    else:
        first_date = datetime.datetime.now() - datetime.timedelta(days=7)
        second_date = datetime.datetime.now()

    query_set = Order.objects.filter(order_date__range=[first_date, second_date]) \
        .values('order_date__date') \
        .annotate(
        total_sale=Sum(
            F('order_detail__quantity') *
            F('order_detail__price')
        )
    )

    return render(request, 'result.html', {'query_set': query_set})


def monthly_sales(request):
    first_date = datetime.datetime.now() - datetime.timedelta(days=365)
    second_date = datetime.datetime.now()

    query_set = Order.objects.filter(order_date__range=[first_date, second_date]) \
        .annotate(
        month=TruncMonth('order_date'),
    ) \
        .values('month') \
        .annotate(
        total_sale=Sum(
            F('order_detail__quantity') *
            F('order_detail__price')
        )
    ) \
        .order_by('-month')

    return render(request, 'result.html', {'query_set': query_set})


def yearly_sales(request):
    query_set = Order.objects.all().annotate(
        year=TruncYear('order_date'),
    ) \
        .values('year') \
        .annotate(
        total_sale=Sum(
            F('order_detail__quantity') *
            F('order_detail__price')
        )
    ).order_by('-year')

    return render(request, 'result.html', {'query_set': query_set})


def customer_sales(request):
    query_set = Order.objects.all().values('phone_number').annotate(
        total_sale=Sum(
            F('order_detail__quantity') *
            F('order_detail__price')
        )
    ).order_by('-total_sale')
    return render(request, 'result.html', {'query_set': query_set})


def category_sales(request):
    query_set = Order.objects.all().annotate(
        category=F('order_detail__product__category__name'),
    ) \
        .values('category').annotate(
        total_sale=Sum(
            F('order_detail__quantity') *
            F('order_detail__price')
        )
    ).order_by('-total_sale')
    return render(request, 'result.html', {'query_set': query_set})


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")
