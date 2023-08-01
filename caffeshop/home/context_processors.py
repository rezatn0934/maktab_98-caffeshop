from .models import Info, Logo


def get_info(request):
    info = Info.objects.filter().first
    return {
        'info': info
    }


def get_logo(request):
    logo = Logo.objects.filter(is_active=True)
    if len(logo) == 1:
        logo = logo.get(is_active=True)
    else:
        logo = None
    return {
        'logo': logo
    }