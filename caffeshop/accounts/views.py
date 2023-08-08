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
from .models import User
from orders.models import Order, Order_detail
from utils import send_otp_code
import datetime


# Create your views here.

class StaffLogin(View):
    message = None
    form = StaffLoginForm
    html_temp = "login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        context = {"message": self.message, "form": self.form()}
        return render(request, self.html_temp, context=context)

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            phone = cd["phone"]
            user = PhoneAuthBackend().authenticate(request, phone=phone)
            if user is not None:
                request.session["phone"] = phone
                return redirect("verify")
            else:
                message = "Invalid phone number"
        else:
            message = "wrong input"

        context = {"message": message, "form": self.form()}
        return render(request, self.html_temp, context=context)


class Verify(View):
    message = None
    form = VerifyCodeForm
    html_temp = "verify.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
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
            code = cd["code"]
            phone = request.session["phone"]
            otp_key = request.session.get("otp_code")
            otp_valid_date = request.session.get("otp_valid_date")
            if otp_key is not None and otp_valid_date is not None:
                valid_until = datetime.datetime.fromisoformat(otp_valid_date)
                if valid_until > timezone.now():
                    if code == otp_key:
                        user = User.objects.get(phone=phone)
                        login(request, user, backend='accounts.authentication.PhoneAuthBackend')
                        del request.session["otp_code"]
                        del request.session["otp_valid_date"]
                        return redirect("dashboard")
                    else:
                        message = "Invalid OTP"
                else:
                    message = "OTP has been expired"
            else:
                message = "Start from here!"
        else:
            message = "wrong input"

        form = self.form()
        context = {"message": message, "form": form}
        return render(request, self.html_temp, context=context)


class Dashboard(View):

    # @method_decorator(login_required)
    def get(self, request):
        return render(request, "dashboard.html")


class Orders(View):
    # @method_decorator(login_required)
    def get(self, request):
        sort = request.GET.get('sort', 'title')
        order = request.GET.get('order', 'asc')
        if sort == 'id' or sort == 'phone_number' or sort == 'order_date' or sort == 'last_modify' or \
                sort == 'table_number' or sort == 'status' or sort == 'payment':
            sort_param = sort if order == 'asc' else '-' + sort
            orders = Order.objects.all().order_by(sort_param)
        else:
            orders = Order.objects.all().order_by('order_date')

        context = {
            'order': 'desc' if order == 'asc' else 'asc',
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

        paginator = Paginator(orders, 5)
        page_number = request.GET.get('page', 1)
        orders = paginator.get_page(page_number)
        context['orders'] = orders
        context['page'] = page_number
        print(request.path)
        return render(request, 'orders_list.html', context)


class OrderDetailView(View):

    # @method_decorator(login_required)
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

    # @method_decorator(login_required)
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
