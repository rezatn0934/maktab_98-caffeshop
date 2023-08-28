from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from .models import Product, Category
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest


# Create your views here.

class Menu(ListView):
    template_name = 'menu/menu.html'
    model = Product
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductView(DetailView):
    template_name = 'menu/product.html'
    model = Product
    context_object_name = 'product'


def search_product_view(request):
    if request.method == 'GET':
        search_term = request.GET.get('search')
        template = 'menu/search.html'
        items = []
        if isinstance(search_term, str):
            template = 'menu/search_results.html'
            if search_term := search_term.strip():
                # if request.headers.get('HX-Request') == 'true':
                items = Product.objects.annotate(similarity=Greatest(
                    TrigramSimilarity("name", string=search_term),
                    TrigramSimilarity("description", string=search_term),
                )).filter(similarity__gt=0).order_by("-similarity")
                if not items.exists():
                    items = ["Nothing Was Found"]

        return render(request, template, context={'items': items})
