from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Category, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    query = request.GET.get("q")
    if query:
        products = products.filter(name__icontains=query)

    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "store/product_list.html", {
        "categories": categories,
        "category": category,
        "page_obj": page_obj,
        "query": query or "",
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "store/product_detail.html", {"product": product})
