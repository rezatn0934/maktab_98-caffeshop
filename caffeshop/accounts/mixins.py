from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

def chart_access_check(user):
    return user.groups.filter(name__in=['Managers', 'Supervisiors', 'Cashier'])
