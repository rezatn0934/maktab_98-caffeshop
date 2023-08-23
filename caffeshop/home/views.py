from django.views.generic.list import ListView

from menu.models import Category, Product
from .models import Gallery, About


# Create your views here.


class HomeView(ListView):
    template_name = 'home/home.html'
    model = Category
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery'] = Gallery.objects.filter(is_active=True)
        qs = About.objects.filter(is_active=True)
        if qs.exists():
            context['about'] = qs.first
        return context
