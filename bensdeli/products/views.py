from django.shortcuts import render

# Create your views here.
def products_view(request):
    return render(request, 'products/products_view.html')