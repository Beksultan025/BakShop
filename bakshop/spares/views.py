from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import redirect, render

from .models import Product


def index(request):
    products = Product.objects.filter(in_stock=True)
    q = request.GET.get("q", "").strip()
    if q:
        products = products.filter(
            Q(name__icontains=q) | Q(brand__icontains=q) | Q(car__icontains=q)
        )
    return render(request, 'main/main.html', {"products": products, "q": q})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})