from django.shortcuts import render, redirect, get_object_or_404
import os
from .forms import ProductForm, ReviewForm
from .models import Product, Review


# Create your views here.
def index_view(request):
    products = Product.objects.all()
    return render(request, "products/index.html", {"products": products})


def product_view(request, pk):
    product = get_object_or_404(Product, id=pk)
    form = ReviewForm()
    reviews = product.reviews.all()
    average_rating = calculate_average_rating(reviews)
    return render(request, "products/product.html",
        {
            "product": product,
            "form": form,
            "reviews": reviews,
            "average_rating": average_rating
        })


def calculate_average_rating(reviews):
    if len(reviews) == 0:
        return "no rating"
    
    sum_rating = 0
    nbr_reviews = 0
    for review in reviews:
        sum_rating += review.rating
        nbr_reviews += 1
    
    return sum_rating / nbr_reviews

def submit_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        product_id = request.POST.get('product_id')
        if form.is_valid():
            product_id = request.POST.get('product_id')
            review = form.save(commit=False)
            review.product_id = product_id
            review.save()
            return redirect('product_view', pk=product_id)
        return redirect('product_view', pk=product_id)
    
    return redirect("index_view")


def internal_view(request):
    # check if user is logged in in session
    try:
        logged_In = request.session["loggedIn"]
    except:
        return redirect("login_view")

    if request.session["loggedIn"] == "True":
        if request.method == "GET":
            products = Product.objects.all()
            return render(request, "products/internal.html", {"products": products})
        if request.method == "POST":
            product_id = request.POST.get("product_id")
            instance = Product.objects.get(id=product_id)
            instance.delete()
            return redirect("internal_view")
    else:
        return redirect("index_view")


def internal_create(request):
    # check if user is logged in in session
    try:
        logged_In = request.session["loggedIn"]
    except:
        return redirect("login_view")

    if request.session["loggedIn"] == "True":
        if request.method == "POST":
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect("internal_view")

        else:
            form = ProductForm()
        return render(request, "products/internal_create.html", {"form": form})
    else:
        return redirect("index_view")


def internal_edit(request, pk):
    # check if user is logged in in session
    try:
        logged_In = request.session["loggedIn"]
    except:
        return redirect("login_view")

    instance = Product.objects.get(id=pk)
    if request.session["loggedIn"] == "True":
        if request.method == "POST":
            form = ProductForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                form.save()
                return redirect("internal_view")

        else:
            form = ProductForm(instance=instance)
        return render(request, "products/internal_edit.html", {"form": form})
    else:
        return redirect("index_view")


def login_view(request):
    if request.method == "GET":
        return render(request, "products/login.html", {"error": ""})

    if request.method == "POST":
        entered_password = request.POST.get("password")
        if (
            entered_password == os.environ.get("BEN_PASSWORD")
            and entered_password != ""
        ):
            request.session["loggedIn"] = "True"
            return redirect("internal_view")
        else:
            return render(
                request,
                "products/login.html",
                {"error": "You entered the wrong password, who you?"},
            )
