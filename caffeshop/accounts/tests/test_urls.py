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
