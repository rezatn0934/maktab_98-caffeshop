from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views import View

from .authentication import PhoneAuthBackend
from .form import StaffLoginForm, VerifyCodeForm, OrderDetailUpdateForm
from orders.models import Order, Order_detail
from utils import send_otp_code, check_is_authenticated

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
            message = "Wrong input, Phone number Should Start Like 09123456789"

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
            main_otp = request.session.get("otp_code")
            otp_valid_date = request.session.get("otp_valid_date")
            if main_otp is not None and otp_valid_date is not None:
                valid_until = datetime.datetime.fromisoformat(otp_valid_date)
                if valid_until > timezone.now():
                    user = PhoneAuthBackend().authenticate(request, phone=phone,
                                                           user_input_otp=user_input_otp,
                                                           main_otp=main_otp)
                    if user is not None:
                        login(request, user, backend='accounts.authentication.PhoneAuthBackend')
                        del request.session["otp_code"]
                        del request.session["otp_valid_date"]
                        return redirect("dashboard")
                    else:
                        message = "Invalid Phone Number or OTP"
                else:
                    message = "OTP has been expired"
            else:
                message = "Start from here!"
        else:
            message = "Wrong input"

        form = self.form()
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
        print(request.path)
        return render(request, 'orders_list.html', context)


class OrderDetailView(View):

    @method_decorator(login_required)
    def get(self, request, pk):
        create_order_form = OrderDetailUpdateForm()
        order = Order.objects.get(id=pk)
        order_details = Order_detail.objects.filter(order=pk)
        order_details = map(lambda order_detail: (
            order_detail.id, order_detail.total_price, OrderDetailUpdateForm(instance=order_detail)),
                            order_details)
        context = {
            'order': order,
            'order_details': order_details,
            'creat_form': create_order_form,
        }

        return render(request, 'order_detail.html', context)

    @method_decorator(login_required)
    def post(self, request, pk):
        if 'update' in request.POST:
            order_detail = Order_detail.objects.get(id=pk)
            form = OrderDetailUpdateForm(request.POST, instance=order_detail)
            if form.is_valid():
                form.save()
                return redirect('order_detail', order_detail.order.id)
            else:
                return redirect('order_detail', order_detail.order.id)


@login_required
def confirm_order(request, pk):
    if request.method == 'GET':
        order = Order.objects.filter(id=pk)
        if order:
            order = order.get(id=pk)
            order.status = 'A'
            order.save()
            return redirect('order_list')
        else:
            message = 'Order not found'
            return redirect('order_detail', pk)


@login_required
def cancel_order(request, pk):
    if request.method == 'GET':
        order = Order.objects.filter(id=pk)
        if order:
            order = order.get(id=pk)
            order.status = 'C'
            order.save()
            return redirect('order_list')
        else:
            message = 'Order not found'
            return redirect('order_detail', pk)


@login_required
def delete_order_detail(request, pk):
    if request.method == 'GET':
        order_detail = Order_detail.objects.filter(id=pk)
        if order_detail:
            order_detail = order_detail.get(id=pk)
            order = order_detail.order
            order_detail.delete()
            return redirect('order_detail', order.id)
        else:
            return redirect(request.path)


class CreateOrder(View):
    @method_decorator(login_required)
    def post(self, request, pk):
        order = Order.objects.get(id=pk)
        form = OrderDetailUpdateForm(request.POST)
        if form.is_valid():
            order_detail = form.save(commit=False)
            order_detail.order = order
            order_detail.price = order_detail.product.price
            order_detail.save()
        else:
            message = 'Invalid input'

        return redirect('order_detail', pk)


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

