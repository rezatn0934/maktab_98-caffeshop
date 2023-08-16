from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.views import View
from .models import Product, Category


# Create your views here.

class Menu(ListView):
    template_name = 'menu/menu.html'
    model = Product
    context_object_name ='products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
 

class ProductView(DetailView):
    template_name = 'menu/product.html'
    model = Product
    context_object_name ='product'


def search_product_view(request):
    if request.method == 'GET':
        search_query = request.GET.get('search')
        search_result = None
        message = None
        if search_query:
            search_result = Product.objects.filter(Q(name__icontains=search_query) |
                                                   Q(description__icontains=search_query) |
                                                   Q(category__name__icontains=search_query)).distinct()
            if not search_result.exists():
                message = f"Nothing was found for {search_query}"

        context = {'search_result': search_result, "message": message}
        return render(request, 'menu/search.html', context=context)

