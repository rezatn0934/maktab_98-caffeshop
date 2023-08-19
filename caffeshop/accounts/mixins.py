from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin , UserPassesTestMixin

class ChartAccessMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.groups.filter(name__in=['Managers', 'Supervisiors', 'Cashier'])


