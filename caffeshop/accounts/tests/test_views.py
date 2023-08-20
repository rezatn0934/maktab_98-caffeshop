from django.contrib.auth.models import AnonymousUser, Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from orders.models import Order, Order_detail, Table
from menu.models import Product, Category
from accounts.views import (
    StaffLogin,
    Verify,
)

#
# class TestStaffLogin(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create(
#             phone='09038916990',
#             password='reza123456',
#             first_name='reza',
#             last_name='teymouri'
#         )
#         self.factory = RequestFactory()
#
#     def test_staff_login_GET_authenticate(self):
#         request = self.factory.get(reverse('login'))
#         request.user = self.user
#         response = StaffLogin.as_view()(request)
#         self.assertEqual(response.status_code, 302)
#
#     def test_staff_login_GET_anonymous(self):
#         request = self.factory.get(reverse('login'))
#         request.user = AnonymousUser()
#         response = StaffLogin.as_view()(request)
#         self.assertEqual(response.status_code, 200)
#
#     def test_staff_login_POST_valid(self):
#         response = self.client.post(reverse('login'), data={'phone': '09038916990'})
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, reverse('verify'))
#
#     def test_staff_login_POST_invalid(self):
#         response = self.client.post(reverse('login'), data={'phone': 'gfhbjnh'})
#         self.assertEqual(response.status_code, 200)
#         self.failIf(response.context['form'].is_valid())
#         self.assertEqual(response.context['message'],
#                          'Wrong input, Phone number Should Start 11 digits Like 09*********')
#         self.assertFormError(form=response.context['form'], field='phone', errors='Enter a valid value.')
#
#
# class TestVerify(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create(
#             phone='09038916990',
#             password='reza123456',
#             first_name='reza',
#             last_name='teymouri'
#         )
#         self.factory = RequestFactory()
#
#     def test_verify_GET_authenticate(self):
#         request = self.factory.get(reverse('verify'))
#         request.user = self.user
#         response = Verify.as_view()(request)
#         self.assertEqual(response.status_code, 302)
#
#     def test_verify_GET_anonymous(self):
#         request = self.factory.get(reverse('verify'))
#         request.user = AnonymousUser()
#         middleware = SessionMiddleware(lambda request: None)
#         middleware.process_request(request)
#         request.session['phone'] = '09038916990'
#         request.session.save()
#         response = Verify.as_view()(request)
#         self.assertEqual(response.status_code, 200)
#         del request.session['phone']
#
#     def test_verify_GET_anonymous_not_phone(self):
#         request = self.factory.get(reverse('verify'))
#         request.user = AnonymousUser()
#         middleware = SessionMiddleware(lambda request: None)
#         middleware.process_request(request)
#         request.session.save()
#         response = Verify.as_view()(request)
#         self.assertEqual(response.status_code, 302)
#
#     def test_verify_POST_invalid(self):
#         response = self.client.post(reverse('verify'), data={'otp_code': 'jjgh'})
#         self.assertEqual(response.status_code, 200)
#         self.failIf(response.context['form'].is_valid())
#         self.assertEqual(response.context['message'],
#                          'Wrong Input')
#         self.assertFormError(form=response.context['form'], field='otp_code', errors='Enter a valid value.')
#
#     def test_verify_POST_valid(self):
#         request = self.factory.post(reverse('verify'), data={'otp_code': '123456'})
#         middleware = SessionMiddleware(lambda request: None)
#         request.user = AnonymousUser()
#         middleware.process_request(request)
#         request.session['otp_code'] = '123456'
#         request.session['phone'] = '09038916990'
#         request.session['otp_valid_date'] = str(timezone.now())
#         valid_date = timezone.now() + timezone.timedelta(minutes=1)
#         request.session["otp_valid_date"] = str(valid_date)
#         request.session.save()
#         setattr(request, '_messages', FallbackStorage(request))
#         response = Verify.as_view()(request)
#         self.assertEqual(response.status_code, 302)
#
#     def test_verify_POST_unknown_user(self):
#         request = self.factory.post(reverse('verify'), data={'otp_code': '123456'})
#         middleware = SessionMiddleware(lambda request: None)
#         request.user = AnonymousUser()
#         middleware.process_request(request)
#         request.session['phone'] = '09198470934'
#         request.session.save()
#         setattr(request, '_messages', FallbackStorage(request))
#         response = Verify.as_view()(request)
#         self.assertEqual(response.status_code, 200)
#
#     def test_verify_POST_invalid_otp_code(self):
#         request = self.factory.post(reverse('verify'), data={'otp_code': '123456'})
#         middleware = SessionMiddleware(lambda request: None)
#         request.user = AnonymousUser()
#         middleware.process_request(request)
#         request.session['otp_code'] = '123458'
#         request.session['phone'] = '09038916990'
#         request.session['otp_valid_date'] = str(timezone.now())
#         valid_date = timezone.now() + timezone.timedelta(minutes=1)
#         request.session["otp_valid_date"] = str(valid_date)
#         request.session.save()
#         setattr(request, '_messages', FallbackStorage(request))
#         response = Verify.as_view()(request)
#         self.assertEqual(response.status_code, 200)
#
#     def test_verify_POST_invalid_otp_date(self):
#         request = self.factory.post(reverse('verify'), data={'otp_code': '123456'})
#         middleware = SessionMiddleware(lambda request: None)
#         request.user = AnonymousUser()
#         middleware.process_request(request)
#         request.session['otp_code'] = '123456'
#         request.session['phone'] = '09038916990'
#         request.session['otp_valid_date'] = str(timezone.now())
#         request.session.save()
#         setattr(request, '_messages', FallbackStorage(request))
#         response = Verify.as_view()(request)
#         self.assertEqual(response.status_code, 200)
#
#     def test_verify_POST_without_otp_code(self):
#         request = self.factory.post(reverse('verify'), data={'otp_code': '123456'})
#         middleware = SessionMiddleware(lambda request: None)
#         request.user = AnonymousUser()
#         middleware.process_request(request)
#         request.session['otp_code'] = '123456'
#         request.session['phone'] = '09038916990'
#         request.session.save()
#         setattr(request, '_messages', FallbackStorage(request))
#         response = Verify.as_view()(request)
#         self.assertEqual(response.status_code, 200)
#
#
# class TestDashboard(TestCase):
#
#     def setUp(self):
#         self.table = Table.objects.create(name='orchid', Table_number=4, occupied=True)
#         self.order = Order.objects.create(
#             payment='P', status='A', phone_number='09152593858', table_number=self.table)
#         self.product = Product.objects.create(category=Category.objects.create(name='Drinks'), name='Tea',
#                                               description='drinks', price=5.00)
#         self.order_detail = Order_detail.objects.create(
#             order=self.order, product=self.product, quantity=4)
#
#         self.client = Client()
#         self.user = User.objects.create_user(
#             phone='09038916990',
#             password='reza123456',
#         )
#
#     def tearDown(self):
#         self.order_detail.delete()
#         self.product.delete()
#         self.order.delete()
#         self.table.delete()
#
#     def test_dashboard_GET(self):
#         self.client.force_login(self.user)
#         response = self.client.get(reverse('dashboard'))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.context.get('total_sale')['total_sale'], 20.0)
#         self.assertTemplateUsed(response, 'dashboard.html')


class TestOrders(TestCase):

    @classmethod
    def setUpTestData(cls):
        content_type = ContentType.objects.get_for_model(Order)
        order_permission = Permission.objects.filter(content_type=content_type)
        manager_group, created = Group.objects.get_or_create(name="Managers")
        manager_group.permissions.add(*order_permission)

    def setUp(self):
        self.table = Table.objects.create(name='orchid', Table_number=4, occupied=True)
        self.table2 = Table.objects.create(name='rose', Table_number=3, occupied=True)
        self.order = Order.objects.create(
            payment='P', status='A', phone_number='09152593858', table_number=self.table)
        self.order2 = Order.objects.create(
            payment='U', status='A', phone_number='09198470934', table_number=None)
        self.product = Product.objects.create(category=Category.objects.create(name='Drinks'), name='Tea',
                                              description='drinks', price=5.00)
        self.order_detail = Order_detail.objects.create(
            order=self.order, product=self.product, quantity=4)
        self.order_detail2 = Order_detail.objects.create(
            order=self.order2, product=self.product, quantity=3)
        self.client = Client()
        self.password = 'reza123456'
        self.user = User.objects.create_user(
            phone='09198470934',
            password=self.password,
        )
        self.manager_group = Group.objects.get(name='Managers')

    def tearDown(self):
        self.order_detail.delete()
        self.order_detail2.delete()
        self.product.delete()
        self.order.delete()
        self.order2.delete()
        self.table.delete()
        self.table2.delete()
        self.user.delete()

    def test_orders_GET_has_perm(self):
        self.user.groups.add(self.manager_group)
        self.client.login(phone=self.user.phone, password=self.password)
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.order, response.context['orders'])
        self.assertTemplateUsed(response, 'orders_list.html')

    def test_orders_GET_dont_has_perm(self):
        self.client.login(phone=self.user.phone, password=self.password)
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 403)

    def test_orders_GET_sort_by_id_asc(self):
        self.user.groups.add(self.manager_group)
        self.client.login(phone=self.user.phone, password=self.password)
        data = {'sort': 'id', 'orderp': 'asc'}
        response = self.client.get(reverse('order_list'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['orders']), 2)
        self.assertTemplateUsed(response, 'orders_list.html')

    def test_orders_GET_sort_by_order_date_desc(self):
        self.user.groups.add(self.manager_group)
        self.client.login(phone=self.user.phone, password=self.password)
        data = {'sort': 'order_date', 'orderp': 'desc'}
        response = self.client.get(reverse('order_list'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['orders']), 2)
        self.assertTemplateUsed(response, 'orders_list.html')

    def test_orders_GET_filter_tabel_name(self):
        self.user.groups.add(self.manager_group)
        self.client.login(phone=self.user.phone, password=self.password)
        data = {'search': 'search', 'filter1': 'orchid', 'flexRadioDefault': 'table_number'}
        response = self.client.get(reverse('order_list'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['orders']), 1)
        self.assertTemplateUsed(response, 'orders_list.html')

    def test_orders_GET_filter_tabel_name_None(self):
        self.user.groups.add(self.manager_group)
        self.client.login(phone=self.user.phone, password=self.password)
        data = {'search': 'search', 'filter1': '', 'flexRadioDefault': 'table_number'}
        response = self.client.get(reverse('order_list'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['orders']), 1)
        self.assertTemplateUsed(response, 'orders_list.html')

    def test_orders_GET_filter_phone_number(self):
        self.user.groups.add(self.manager_group)
        self.client.login(phone=self.user.phone, password=self.password)
        data = {'search': 'search', 'filter1': '09152593858', 'flexRadioDefault': 'phone_number'}
        response = self.client.get(reverse('order_list'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['orders']), 1)
        self.assertTemplateUsed(response, 'orders_list.html')

    def test_orders_GET_filter_order_second_date(self):
        self.user.groups.add(self.manager_group)
        self.client.login(phone=self.user.phone, password=self.password)
        order_date = timezone.now() - timezone.timedelta(days=1)
        data = {'filter': 'filter', 'first_date': str(order_date)}
        response = self.client.get(reverse('order_list'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['orders']), 2)
        self.assertTemplateUsed(response, 'orders_list.html')

    def test_orders_GET_filter_order_first_date(self):
        self.user.groups.add(self.manager_group)
        self.client.login(phone=self.user.phone, password=self.password)
        data = {'paid': self.order2.id}
        response = self.client.get(reverse('order_list'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.get(id=self.order2.id).payment, 'P')
        self.assertTemplateUsed(response, 'orders_list.html')
