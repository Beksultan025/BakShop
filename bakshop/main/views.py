# ===== 1. ИМПОРТЫ: замени блок импортов вверху views.py на этот =====
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm, OrderForm
from .models import Product, Order
from django.db.models import Min, Max, Avg


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

staff_required = user_passes_test(
    lambda u: u.is_active and u.is_staff, login_url="login"
)


@login_required
def after_login(request):
    if request.user.is_staff:
        return redirect("panel_dashboard")
    return redirect("index")

@staff_required
def panel_analytics(request):
    prices = Product.objects.aggregate(
        min_price=Min("price"),
        avg_price=Avg("price"),
        max_price=Max("price"),
    )
    return render(request, "main/panel_analytics.html", {"prices": prices})

@staff_required
def panel_dashboard(request):
    context = {
        "total": Product.objects.count(),
        "in_stock": Product.objects.filter(in_stock=True).count(),
        "out_stock": Product.objects.filter(in_stock=False).count(),
        "users": User.objects.count(),
        "latest": Product.objects.all()[:5],
    }
    return render(request, "panel/panel_dashboard.html", context)


@staff_required
def panel_list(request):
    products = Product.objects.all()
    q = request.GET.get("q", "").strip()
    if q:
        products = products.filter(
            Q(name__icontains=q) | Q(brand__icontains=q) | Q(car__icontains=q)
        )
    return render(request, "panel/panel_list.html", {"products": products, "q": q})


@staff_required
def panel_add(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("panel_list")
    return render(request, "panel/panel_form.html", {"form": form, "title": "Новый товар"})


@staff_required
def panel_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("panel_list")
    return render(request, "panel/panel_form.html", {"form": form, "title": "Изменить товар"})


@staff_required
def panel_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        if product.photo:
            product.photo.delete(save=False)
        product.delete()
        return redirect("panel_list")
    return render(request, "panel/panel_delete.html", {"product": product})


@staff_required
def panel_analytics(request):
    # TODO: посчитай статистику здесь и передай в шаблон через context
    return render(request, "panel/panel_analytics.html")

def buy(request, pk):
    product = get_object_or_404(Product, pk=pk, in_stock=True)
    form = OrderForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        d = form.cleaned_data
        Order.objects.create(
            product=product,
            product_name=product.name,
            price=product.price,
            quantity=d["quantity"],
            name=d["name"],
            phone=d["phone"],
            comment=d["comment"],
        )
        return redirect("buy_success")

    return render(request, "main/buy.html", {"product": product, "form": form})

def buy_success(request):
    return render(request, "main/buy_success.html")

def cart_add(request, pk):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=pk, in_stock=True)
        cart = request.session.get("cart", {})
        key = str(product.pk)
        cart[key] = cart.get(key, 0) + 1
        request.session["cart"] = cart
    return redirect("cart_detail")


def cart_remove(request, pk):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        cart.pop(str(pk), None)
        request.session["cart"] = cart
    return redirect("cart_detail")


def cart_detail(request):
    cart = request.session.get("cart", {})
    products = Product.objects.filter(pk__in=cart.keys())
    items = []
    total = 0
    for p in products:
        qty = cart[str(p.pk)]
        subtotal = p.price * qty
        total += subtotal
        items.append({"product": p, "qty": qty, "subtotal": subtotal})
    return render(request, "main/cart.html", {"items": items, "total": total})
