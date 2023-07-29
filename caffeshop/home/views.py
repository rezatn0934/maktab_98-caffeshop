from django.shortcuts import render
from menu.models import Category, Product,ParentCategory

# Create your views here.


def home(request):
    parentcat = ParentCategory.objects.all()
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'home.html', {'categories': categories, 'products': products, 'parentcategories': parentcat})