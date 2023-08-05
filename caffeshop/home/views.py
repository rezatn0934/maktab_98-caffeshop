from menu.models import Category, Product, ParentCategory
from django.shortcuts import render
from .models import Gallery, About


# Create your views here.


def home(request):
    gallery = Gallery.objects.filter(is_active=True)
    parentcat = ParentCategory.objects.all()
    categories = Category.objects.all()
    products = Product.objects.all()
    about = About.objects.get(is_active=True)
    context = {'categories': categories, 'products': products,
               'parentcategories': parentcat, 'gallery': gallery, 'about': about}
    return render(request, 'home/home.html', context=context)
