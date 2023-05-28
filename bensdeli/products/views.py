from django.shortcuts import render, redirect, get_object_or_404
import os
from .forms import ProductForm, ReviewForm, SizeOptionForm
from .models import Product, Review, SizeOption


# Create your views here.
def index_view(request):
    products = Product.objects.all()
    return render(request, "products/index.html", {"products": products})


def product_view(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except:
        product = Product.objects.first()
    form = ReviewForm(initial={'user': request.user})
    reviews = product.reviews.all()
    average_rating = calculate_average_rating(reviews)

    # Find the prev and next product
    previous_product = Product.objects.filter(id__lt=product.id).order_by('-id').first()
    next_product = Product.objects.filter(id__gt=product.id).first()

    # get biggest size option for product
    biggest_size_option = product.sizes.order_by('-size').first()

    return render(request, "products/product.html",
        {
            "product": product,
            "biggest_size_option": biggest_size_option,
            "form": form,
            "reviews": reviews,
            "average_rating": average_rating,
            "previous_product_id": previous_product.id if previous_product else None,
            "next_product_id": next_product.id if next_product else None
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
        form = ReviewForm(request.POST, initial={'user': request.user})
        product_id = request.POST.get('product_id')
        if form.is_valid():
            review = form.save(commit=False)
            review.product_id = product_id
            review.save()
            return redirect('product_view', pk=product_id)
        return redirect('product_view', pk=product_id)

    return redirect("index_view")


def delete_review(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        review_id = request.POST.get('review_id')
        review_user_id = int(request.POST.get('review_user_id'))
        breakpoint()
        if review_user_id == request.user.id:
            review = get_object_or_404(Review, id=review_id)
            review.delete()
            return redirect('product_view', pk=product_id)
        else:
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
            form = SizeOptionForm()
            return render(request, "products/internal.html", {"products": products, "form": form})
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


def internal_create_size_option(request):
    if request.method == "POST":
        size_option_form = SizeOptionForm(request.POST)
        if size_option_form.is_valid():
            size_option_form.save()
            return redirect("internal_view")

def internal_delete_size_option(request):
    if request.method == "POST":
        size_id = request.POST.get("size_id")
        size_option = get_object_or_404(SizeOption, id=size_id)
        product = size_option.product
        size_option.delete()
        return redirect("internal_view")

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
