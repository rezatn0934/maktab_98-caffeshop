from django.shortcuts import render
from django.views.generic import  DetailView, View
from .models import Product, Category
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest


# Create your views here.

class Menu(View):
    template_name = 'menu/menu.html'
    model = Product

    def get(self, request):
        search_term = request.GET.get('search')

        items = self.model.objects.all()
        if request.headers.get('HX-Request') == 'true':
            self.template_name = 'menu/search_results.html'
            if isinstance(search_term, str):
                if search_term != '':
                    items = Product.objects.annotate(similarity=Greatest(
                        TrigramSimilarity("name", string=search_term),
                        TrigramSimilarity("description", string=search_term),
                    )).filter(similarity__gt=0).order_by("-similarity")

                    if not items.exists():
                        items = ["Nothing Was Found"]
        context = {'items': items, 'categories': Category.objects.all()}
        return render(request, self.template_name, context=context)


class ProductView(DetailView):
    template_name = 'menu/product.html'
    model = Product
    context_object_name = 'product'
