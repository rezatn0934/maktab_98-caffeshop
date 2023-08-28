from django.shortcuts import render
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
