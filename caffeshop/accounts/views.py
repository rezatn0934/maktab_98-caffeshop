from django.db.models.functions import TruncMonth, TruncDay, TruncHour, ExtractHour, Substr, Cast
from django.db.models import Q, F, Sum, Count, DateField, DateTimeField, CharField
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from .authentication import PhoneAuthBackend
from .mixins import chart_access_check, FilterMixin
from .form import StaffLoginForm, VerifyCodeForm
from orders.models import Order, Order_detail
from utils import send_otp_code, check_is_authenticated
from menu.models import Product

import datetime


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

        context = {"message": message, "form": form}
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
                message = str(e)
                if message == "Login First" or message == "Phone Number Does Not Exist":
                    context = {"message": message, "form": StaffLoginForm}
                    return render(request, "login.html", context=context)
        else:
            message = "Wrong Input"

        context = {"message": message, "form": form}
        return render(request, self.html_temp, context=context)


class Dashboard(LoginRequiredMixin, View):

    def get(self, request):
        total_sale = Order.objects.aggregate(
            total_sale=Sum(
                F('order_detail__quantity') *
                F('order_detail__price')
            )
        )
        query_set = Order.objects.annotate(
            hour=ExtractHour("order_date")).values(
            "hour").annotate(count=Count('id')).order_by('hour')
        return render(request, "dashboard.html", {"total_sale": total_sale, 'query_set': query_set})


class Orders(LoginRequiredMixin, PermissionRequiredMixin, FilterMixin, View):
    permission_required = ['orders.view_order']

    def get(self, request):
        context, orders = self.check_sort(request)
        context, orders = self.check_search(request=request, context=context, orders=orders)


        paginator = Paginator(orders, 5)
        page_number = request.GET.get('page', 1)
        orders = paginator.get_page(page_number)
        context['orders'] = orders
        context['page'] = page_number
        return render(request, 'orders_list.html', context)

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order_detail.html'
    context_object_name= "order"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_details'] = Order_detail.objects.filter(order=self.kwargs['pk'])
        context['products'] = Product.objects.filter(is_active=True)
        return context


class UpdateOrderItem(PermissionRequiredMixin, UpdateView, DetailView):
    permission_required = ['orders.add_order_detail']
    model = Order_detail
    fields = ['product', 'quantity']

    def form_valid(self, form):
        messages.success(self.request, 'Order item has been successfully updated.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Form input is not valid')
        return redirect(reverse_lazy('order_detail', args=[self.get_object().order.id]))

    def get_success_url(self):
        return reverse_lazy('order_detail', args=[self.get_object().order.id])
      
      
class CreateOrderItem(PermissionRequiredMixin, CreateView):
    permission_required = ['orders.add_order_detail']
    model = Order_detail
    fields = ['product', 'quantity', 'order']
    template_name = 'order_detail.html'

    def form_valid(self, form):
        order = form.cleaned_data['order'].id
        messages.success(self.request, f"Order item has been successfully added to Order {order}")
        self.success_url = reverse_lazy('order_detail', args=[order])
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Form input is not valid')   
        return super().form_invalid(form)

@login_required
@permission_required(['orders.change_order_status'])
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
            return redirect('order_list')


@login_required
@permission_required('orders.change_order_status')
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
            return redirect('order_list')


@login_required
@permission_required(['orders.change_order_detail'])
def delete_order_detail(request, pk):
    if request.method == 'GET':
        order_detail = Order_detail.objects.filter(id=pk)
        if order_detail:
            order_detail = order_detail.get(id=pk)
            order = order_detail.order
            order_detail.delete()
            messages.warning(request, f'Order item {pk} has been deleted!')
            return redirect('order_detail', order.id)
        else:
            messages.error(request, f'Order items {pk} not found')
            return redirect('order_list')


@login_required
@user_passes_test(chart_access_check)
def most_popular(request):
    if 'filter' in request.GET:
        first_date = request.GET.get('first_date')
        second_date = request.GET.get('second_date')
        limit = int(request.GET.get('quantity'))
        query_set = Order_detail.objects.filter(
            order__order_date__range=[first_date, second_date]).values('product').annotate(
            order_count=Count('id')).annotate(
            name=F('product__name')).order_by(
            '-order_count')[:limit]

    else:
        limit = 5
        query_set = Product.objects.all().annotate(
            order_count=Count('order_detail')
        ).order_by('-order_count')[:limit]

    context = {'query_set': query_set}

    return render(request, 'analytics/most_popular.html', context=context)


@login_required
@user_passes_test(chart_access_check)
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


@login_required
@user_passes_test(chart_access_check)
def top_selling(request):
    if 'filter' in request.GET:
        first_date = request.GET.get('first_date')
        second_date = request.GET.get('second_date')
        query_set = Order_detail.objects.filter(order__payment='P',
                                                order__order_date__range=[first_date, second_date]).values(
            "product").annotate(total_sale=Sum(F('quantity') * F('price'))).annotate(name=F('product__name')).order_by(
            '-total_sale')[:5]
    else:

        query_set = Product.objects.filter(order_detail__order__payment='P').annotate(
            total_sale=Sum(
                F('order_detail__quantity') *
                F('order_detail__price')
            )).filter(Q(total_sale__isnull=False)).order_by('-total_sale')[:5]

    return render(request, 'analytics/top_selling.html', {'query_set': query_set})


@login_required
@user_passes_test(chart_access_check)
def hourly_sales(request):
    if 'filter' in request.GET:
        first_date = request.GET.get('first_date')
        second_date = request.GET.get('second_date')
        if not second_date:
            second_date = timezone.now()

    else:
        first_date = timezone.now().date()
        second_date = timezone.now()

    query_set = Order.objects.filter(payment='P', order_date__range=[first_date, second_date]).values(
        hour=Substr(Cast(TruncHour('order_date', output_field=DateTimeField()), output_field=CharField()), 1,
                    19)).annotate(total_sale=Sum(F('order_detail__quantity') * F('order_detail__price'))).order_by(
        'hour')
    return render(request, 'analytics/hourly_sales.html', {'query_set': query_set})


@login_required
@user_passes_test(chart_access_check)
def daily_sales(request):
    if 'filter' in request.GET:
        first_date = request.GET.get('first_date')
        second_date = request.GET.get('second_date')
        if not second_date:
            second_date = timezone.now()
    else:
        first_date = datetime.date(timezone.now().date().year, timezone.now().date().month, 1)
        second_date = timezone.now()

    query_set = Order.objects.filter(payment='P', order_date__range=[first_date, second_date]).values(
        day=Substr(Cast(TruncDay('order_date', output_field=DateField()),
                        output_field=CharField()), 1, 10)).annotate(
        total_sale=Sum(F('order_detail__quantity') * F('order_detail__price'))).order_by('day')

    return render(request, 'analytics/daily_sales.html', {'query_set': query_set})


@login_required
@user_passes_test(chart_access_check)
def monthly_sales(request):
    if 'filter' in request.GET:
        first_date = request.GET.get('first_date')
        second_date = request.GET.get('second_date')
        if not second_date:
            second_date = timezone.now()
    else:
        first_date = datetime.date(timezone.now().date().year, 1, 1)
        second_date = timezone.now()

    query_set = Order.objects.filter(payment='P', order_date__range=[first_date, second_date]).values(month=Substr(
        Cast(TruncMonth('order_date', output_field=DateField()),
             output_field=CharField()), 1, 7)).annotate(
        total_sale=Sum(F('order_detail__quantity') * F('order_detail__price'))).order_by('month')

    return render(request, 'analytics/monthly_sales.html', {'query_set': query_set})


@login_required
@user_passes_test(chart_access_check)
def yearly_sales(request):
    if 'filter' in request.GET:
        first_date = request.GET.get('first_date')
        second_date = request.GET.get('second_date') or timezone.now()
        query_set = Order.objects.filter(payment='P', order_date__range=[first_date, second_date])
    else:
        query_set = Order.objects.filter(payment='P', )

    query_set = query_set.values(year=Substr(
        Cast(TruncMonth('order_date', output_field=DateField()),
             output_field=CharField()), 1, 4)).annotate(
        total_sale=Sum(F('order_detail__quantity') * F('order_detail__price'))).order_by('year')

    return render(request, 'analytics/yearly_sales.html', {'query_set': query_set})


@login_required
@user_passes_test(chart_access_check)
def customer_sales(request):
    limit = 5
    if 'filter' in request.GET:
        first_date = request.GET.get('first_date')
        second_date = request.GET.get('second_date') or timezone.now()
        limit = int(request.GET.get('quantity') or limit)
        query_set = Order.objects.filter(payment='P', order_date__range=[first_date, second_date])
    else:
        query_set = Order.objects.filter(payment='P')

    query_set = query_set.values('phone_number').annotate(
        total_sale=Sum(
            F('order_detail__quantity') *
            F('order_detail__price')
        )
    ).order_by('-total_sale')[:limit]
    return render(request, 'analytics/customer_sales.html', {'query_set': query_set})


@login_required
@user_passes_test(chart_access_check)
def customer_demographic(request):
    query_set = None
    query_set2 = None
    total_spent = 0
    rank = None
    if phone_number := request.GET.get('phone_number'):
        query_set = Order.objects.filter(payment='P', phone_number=phone_number).annotate(
            product=F("order_detail__product__name")).annotate(quantity=F("order_detail__quantity")).annotate(
            price=F("order_detail__price")).values("product").annotate(spent=Sum(F('quantity') * F('price'))).annotate(
            total=Sum('quantity')).order_by("-spent")

        total_spent = query_set.aggregate(total_spent=Sum("spent"))
        query_set2 = Order.objects.filter(payment='P').annotate(
            hour=ExtractHour("order_date")).values(
            "hour").annotate(count=Count('id')).order_by('hour')

        query_set3 = Order.objects.filter(payment='P').values('phone_number').annotate(
            total_sale=Sum(
                F('order_detail__quantity') *
                F('order_detail__price')
            )
        ).order_by('-total_sale')
        for i, obj in enumerate(query_set3):
            if obj['phone_number'] == phone_number:
                rank = i + 1
                break
    context = {'query_set': query_set, "total_spent": total_spent, "query_set2": query_set2, 'rank': rank}
    return render(request, 'analytics/customer_demographic.html', context=context)


@login_required
@user_passes_test(chart_access_check)
def sales_by_category(request):
    first_date = request.GET.get('first_date') or '1970-01-01'
    second_date = request.GET.get('second_date') or timezone.now()
    query_set = Order_detail.objects.filter(order__payment='P').annotate(date=F('order__order_date')) \
        .filter(date__range=[first_date, second_date]) \
        .annotate(category=F("product__category__name")) \
        .values('category') \
        .annotate(total_sale=Sum(F("quantity") * F("price"))).order_by('total_sale')
    context = {'query_set1': query_set}

    return render(request, 'analytics/sales_by_category.html', context=context)


@login_required
@user_passes_test(chart_access_check)
def order_status_report(request):
    lst2 = None
    first_date = "1970-01-01"
    second_date = timezone.now()
    first_date2 = None

    if 'filter' in request.GET:
        first_date = request.GET.get('first_date')
        second_date = (
                datetime.datetime.strptime(first_date, '%Y-%m-%d') + timezone.timedelta(
            days=1)).strftime('%Y-%m-%d')
        if request.GET.get('second_date'):
            first_date2 = request.GET.get('second_date')

            second_date2 = (datetime.datetime.strptime(request.GET.get('second_date'), '%Y-%m-%d') + timezone.timedelta(
                days=1)).strftime('%Y-%m-%d')

            query_set2 = Order.objects.filter(order_date__range=[first_date2, second_date2]).values("status").annotate(
                count=Count("id")).order_by("status")

            lst2 = [0, 0, 0]
            for item in query_set2:
                if item["status"] == "A":
                    lst2[0] = item["count"]
                elif item["status"] == "C":
                    lst2[1] = item["count"]
                elif item["status"] == "P":
                    lst2[2] = item["count"]

    query_set = Order.objects.filter(order_date__range=[first_date, second_date]).values("status").annotate(
        count=Count("id")).order_by("status")

    lst1 = [0, 0, 0]
    for item in query_set:
        if item["status"] == "A":
            lst1[0] = item["count"]
        elif item["status"] == "C":
            lst1[1] = item["count"]
        elif item["status"] == "P":
            lst1[2] = item["count"]

    context = {'lst1': lst1, 'lst2': lst2, "first_date": first_date, "first_date2": first_date2}
    return render(request, 'analytics/order_status_report.html', context=context)


@login_required
@user_passes_test(chart_access_check)
def sales_by_employee_report(request):
    first_date = request.GET.get('first_date') or '1970-01-01'
    second_date = request.GET.get('second_date') or timezone.now()

    if request.GET.get('phone_number'):
        phone_number = request.GET.get('phone_number')
        query_set = Order.objects.filter(
            staff_id__isnull=False, order_date__range=[first_date, second_date]).annotate(
            day=TruncDay("order_date", output_field=DateField())).values(
            "day").annotate(
            count=Count("id")).annotate(
            phone_number_emp=F("staff__phone")).filter(phone_number_emp=phone_number).order_by("-count")
        context = {'query_set2': query_set}
        return render(request, 'analytics/sales_by_employee_report.html', context=context)

    query_set = Order.objects.filter(
        staff_id__isnull=False, order_date__range=[first_date, second_date]).values("staff_id").annotate(
        count=Count("id")).annotate(
        phone_number_emp=F("staff__phone")).order_by("-count")
    context = {'query_set': query_set}
    return render(request, 'analytics/sales_by_employee_report.html', context=context)


@login_required
@user_passes_test(chart_access_check)
def customer_order_history(request):
    context = {}

    if phone_number := request.GET.get('phone_number'):
        first_date = request.GET.get('first_date') or '1970-01-01'
        second_date = request.GET.get('second_date') or timezone.now()
        query_set = Order.objects.filter(order_date__range=[first_date, second_date]) \
            .filter(phone_number=phone_number) \
            .annotate(date=TruncDay("order_date", output_field=DateField())) \
            .values("date") \
            .annotate(count=Count('id')).order_by('count')
        orders = Order.objects.filter(phone_number=phone_number).order_by('-order_date')
        context = {'query_set': query_set, "orders": orders}
    return render(request, 'analytics/customer_order_history.html', context=context)


@login_required
@user_passes_test(chart_access_check)
def product_hour(request):
    first_date = request.GET.get('first_date') or '1970-01-01'
    second_date = request.GET.get('second_date') or timezone.now()

    query_set = Order.objects.filter(payment='P', order_date__range=[first_date, second_date]).annotate(
        hour=ExtractHour('order_date')).annotate(
        product=F("order_detail__product__name")).annotate(
        quantity=F("order_detail__quantity")).values("product", "hour", "quantity").annotate(
        order_count=Count("id")).values("product", "hour").annotate(total_order=(Sum("quantity"))).order_by("hour")
    lst = []
    for index, item in enumerate(query_set):
        if index == 0:
            lst.append(item)
        else:
            if item["hour"] != lst[-1]["hour"]:
                lst.append(item)
            else:
                if item["total_order"] >= lst[-1]["total_order"]:
                    lst.pop()
                    lst.append(item)

    context = {'query_set': lst}
    return render(request, 'analytics/product_hour.html', context=context)


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")
