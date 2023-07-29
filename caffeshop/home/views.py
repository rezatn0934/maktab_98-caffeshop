from django.shortcuts import render
from menu.models import Category, Product

# Create your views here.


def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'home.html', {'categories': categories, 'products': products})