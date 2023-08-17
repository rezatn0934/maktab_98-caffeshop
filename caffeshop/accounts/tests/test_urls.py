from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts import views


class TestUrls(SimpleTestCase):
    def test_login(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, views.StaffLogin)

    def test_verify(self):
        url = reverse('verify')
        self.assertEqual(resolve(url).func.view_class, views.Verify)

    def test_logout(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, views.logout_view)

    def test_dashboard(self):
        url = reverse('dashboard')
        self.assertEqual(resolve(url).func.view_class, views.Dashboard)

    def test_customer_demographic(self):
        url = reverse('customer_demographic')
        self.assertEqual(resolve(url).func, views.customer_demographic)

    def test_most_popular(self):
        url = reverse('most_popular')
        self.assertEqual(resolve(url).func, views.most_popular)

    def test_peak_business_hour(self):
        url = reverse('peak_business_hour')
        self.assertEqual(resolve(url).func, views.peak_business_hour)

    def test_top_selling(self):
        url = reverse('top_selling')
        self.assertEqual(resolve(url).func, views.top_selling)

    def test_hourly_sales(self):
        url = reverse('hourly_sales')
        self.assertEqual(resolve(url).func, views.hourly_sales)

    def test_daily_sales(self):
        url = reverse('daily_sales')
        self.assertEqual(resolve(url).func, views.daily_sales)

    def test_monthly_sales(self):
        url = reverse('monthly_sales')
        self.assertEqual(resolve(url).func, views.monthly_sales)

    def test_yearly_sales(self):
        url = reverse('yearly_sales')
        self.assertEqual(resolve(url).func, views.yearly_sales)

    def test_customer_sales(self):
        url = reverse('customer_sales')
        self.assertEqual(resolve(url).func, views.customer_sales)

    def test_sales_by_category(self):
        url = reverse('sales_by_category')
        self.assertEqual(resolve(url).func, views.sales_by_category)

    def test_order_status_report(self):
        url = reverse('order_status_report')
        self.assertEqual(resolve(url).func, views.order_status_report)

    def test_customer_order_history(self):
        url = reverse('customer_order_history')
        self.assertEqual(resolve(url).func, views.customer_order_history)

    def test_sales_by_employee_report(self):
        url = reverse('sales_by_employee_report')
        self.assertEqual(resolve(url).func, views.sales_by_employee_report)

    def test_product_hour(self):
        url = reverse('product_hour')
        self.assertEqual(resolve(url).func, views.product_hour)

    def test_order_list(self):
        url = reverse('order_list')
        self.assertEqual(resolve(url).func.view_class, views.Orders)

    def test_order_detail(self):
        url = reverse('order_detail', args=(1,))
        self.assertEqual(resolve(url).func.view_class, views.OrderDetailView)

    def test_create_order_detail(self):
        url = reverse('create_order_detail', args=(1,))
        self.assertEqual(resolve(url).func.view_class, views.CreateOrderItem)

    def test_delete_order_item(self):
        url = reverse('delete_order_item', args=(1,))
        self.assertEqual(resolve(url).func, views.delete_order_detail)

    def test_confirm_order(self):
        url = reverse('confirm_order', args=(1,))
        self.assertEqual(resolve(url).func, views.confirm_order)

    def test_cancel_order(self):
        url = reverse('cancel_order', args=(1,))
        self.assertEqual(resolve(url).func, views.cancel_order)
