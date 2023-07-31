from django.shortcuts import render
from menu.models import Category, Product, ParentCategory
from .models import Gallery, BackgroundImage


# Create your views here.


def home(request):
    gallery = Gallery.objects.filter(is_active=True)
    background_image = BackgroundImage.objects.get(is_active=True)
    parentcat = ParentCategory.objects.all()
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {'categories': categories, 'products': products,
               'parentcategories': parentcat, 'gallery': gallery,
               "background_image": background_image}
    return render(request, 'home/home.html', context=context)