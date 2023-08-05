from .models import Info


def get_info(request):
    info = Info.objects.filter().first
    return {
        'info': info
    }