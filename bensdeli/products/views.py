from django.shortcuts import render, redirect
import os
from .forms import ProductForm
from .models import Product


# Create your views here.
def index_view(request):
    products = Product.objects.all()
    return render(request, "products/index.html", {"products": products})


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
