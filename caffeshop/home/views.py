from menu.models import Category, Product
from django.shortcuts import render
from .models import Gallery, About


# Create your views here.


def home(request):
    gallery = Gallery.objects.filter(is_active=True)
    categories = Category.objects.all()
    products = Product.objects.all()
    about = About.objects.filter(is_active=True)
    context = {'categories': categories, 'products': products,
               'gallery': gallery, 'about': about}
    return render(request, 'home/home.html', context=context)
