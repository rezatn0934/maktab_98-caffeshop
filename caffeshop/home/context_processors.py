from .models import Info


def get_info(request):
    qs = Info.objects.filter().first
    return {
        'info': qs
    }