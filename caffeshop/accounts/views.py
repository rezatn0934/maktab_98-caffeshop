from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, F, Sum, Count, DateField, DateTimeField, CharField, TimeField
from django.db.models.functions import TruncMonth, TruncYear, TruncDay, TruncHour, ExtractHour, Substr, Cast

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
        total_sale = Order.objects.aggregate(
            total_sale=Sum(
                F('order_detail__quantity') *
                F('order_detail__price')
            )
        )
        return render(request, "dashboard.html", {"total_sale": total_sale})


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
            order.staff = request.user
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
            order.staff = request.user
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

    context = {'query_set': query_set}

    return render(request, 'analytics/most_popular.html', context=context)


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
    if 'filter' in request.GET:
        first_date = request.GET.get('first_date')
        second_date = request.GET.get('second_date')
        query_set = Order_detail.objects.all().annotate(date=F('order__order_date')).filter(
            date__range=[first_date, second_date]).values("product").annotate(
            total_sale=Sum(F('quantity') * F('price'))).annotate(
            name=F('product__name')).order_by('-total_sale')[:5]
    else:

        query_set = Product.objects.annotate(
            total_sale=Sum(
                F('order_detail__quantity') *
                F('order_detail__price')
            )).filter(Q(total_sale__isnull=False)).order_by('-total_sale')[:5]

    return render(request, 'analytics/top_selling.html', {'query_set': query_set})


def hourly_sales(request):
    if 'filter' in request.GET:
        first_date = request.GET.get('first_date')
        second_date = request.GET.get('second_date')
        if not second_date:
            second_date = timezone.now()

    else:
        first_date = timezone.now().date()
        second_date = timezone.now()

    query_set = Order.objects.filter(order_date__range=[first_date, second_date]) \
        .annotate(
        hour=TruncHour('order_date', output_field=DateTimeField())).values('hour') \
        .annotate(
        total_sale=Sum(
            F('order_detail__quantity') *
            F('order_detail__price'))).order_by('hour')
    return render(request, 'analytics/hourly_sales.html', {'query_set': query_set})


def daily_sales(request):
    if 'filter' in request.GET:
        first_date = request.GET.get('first_date')
        second_date = request.GET.get('second_date')
        if not second_date:
            second_date = timezone.now()
    else:
        first_date = datetime.date(timezone.now().date().year, timezone.now().date().month, 1)
        second_date = timezone.now()

    query_set = Order.objects.filter(order_date__range=[first_date, second_date]) \
        .annotate(
        day=TruncDay('order_date', output_field=DateField())).values('day') \
        .annotate(
        total_sale=Sum(
            F('order_detail__quantity') *
            F('order_detail__price'))).order_by('day')

    return render(request, 'analytics/daily_sales.html', {'query_set': query_set})


def monthly_sales(request):
    if 'filter' in request.GET:
        first_date = request.GET.get('first_date')
        second_date = request.GET.get('second_date')
        if not second_date:
            second_date = timezone.now()
    else:
        first_date = datetime.date(timezone.now().date().year, 1, 1)
        second_date = timezone.now()

    query_set = Order.objects.filter(order_date__range=[first_date, second_date]).values(month=Substr(
        Cast(TruncMonth('order_date', output_field=DateField()),
             output_field=CharField()), 1, 7)).annotate(
        total_sale=Sum(F('order_detail__quantity') * F('order_detail__price'))).order_by('month')

    return render(request, 'analytics/monthly_sales.html', {'query_set': query_set})


def yearly_sales(request):
    if 'filter' in request.GET:
        first_date = request.GET.get('first_date')
        second_date = request.GET.get('second_date') or timezone.now()
        query_set = Order.objects.filter(order_date__range=[first_date, second_date])
    else:
        query_set = Order.objects.all()

    query_set = query_set.values(year=Substr(
        Cast(TruncMonth('order_date', output_field=DateField()),
             output_field=CharField()), 1, 4)).annotate(
        total_sale=Sum(F('order_detail__quantity') * F('order_detail__price'))).order_by('year')

    return render(request, 'analytics/yearly_sales.html', {'query_set': query_set})


def customer_sales(request):
    limit = 5
    if 'filter' in request.GET:
        first_date = request.GET.get('first_date')
        second_date = request.GET.get('second_date') or timezone.now()
        limit = int(request.GET.get('quantity') or limit)
        query_set = Order.objects.filter(order_date__range=[first_date, second_date])
    else:
        query_set = Order.objects.all()

    query_set = query_set.values('phone_number').annotate(
        total_sale=Sum(
            F('order_detail__quantity') *
            F('order_detail__price')
        )
    ).order_by('-total_sale')[:limit]
    return render(request, 'analytics/customer_sales.html', {'query_set': query_set})


def customer_demographic(request):

    phone_number = "09117200513"
    query_set = Order.objects.filter(phone_number=phone_number).annotate(
        product=F("order_detail__product__name")).annotate(quantity=F("order_detail__quantity")).annotate(
        price=F("order_detail__price")).values("product").annotate(spent=Sum(F('quantity') * F('price'))).annotate(
        total=Sum('quantity')).order_by("-spent")

    total_spent = query_set.aggregate(total_spent=Sum("spent"))
    query_set2 = Order.objects.filter(phone_number=phone_number).annotate(
        hour=ExtractHour("order_date")).values(
        "hour").annotate(count=Count('id')).order_by('hour')

    context = {'query_set': query_set, "total_spent": total_spent, "query_set2": query_set2}
    return render(request, 'result.html', context=context)


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

