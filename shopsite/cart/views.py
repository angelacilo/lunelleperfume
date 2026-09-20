from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from store.models import Product
from .cart import Cart


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (ValueError, TypeError):
        quantity = 1
    cart.add(product=product, quantity=quantity)

    if request.headers.get("x-requested-with") == "XMLHttpRequest" or "application/json" in request.headers.get("Accept", ""):
        return JsonResponse({
            "success": True,
            "cart_count": len(cart),
            "cart_total": str(cart.get_total_price()),
            "message": f"{product.name} added to cart! ♡",
        })

    messages.success(request, f"{product.name} added to your cart! ♡")
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or product.get_absolute_url()
    return redirect(next_url)


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/detail.html", {"cart": cart})
