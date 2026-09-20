from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from cart.cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem


def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.content_type == "application/json":
            return JsonResponse({"success": False, "error": "Your cart is empty."}, status=400)
        return redirect("cart:cart_detail")

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            cart.clear()
            request.session["recent_order_id"] = order.id
            if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.content_type == "application/json":
                return JsonResponse({"success": True, "redirect_url": reverse("orders:order_created", kwargs={"order_id": order.id})})
            return redirect("orders:order_created", order_id=order.id)
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.content_type == "application/json":
                return JsonResponse({"success": False, "errors": form.errors}, status=400)
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data["full_name"] = request.user.get_full_name() or request.user.username
        form = OrderCreateForm(initial=initial_data)

    return render(request, "orders/create.html", {"cart": cart, "form": form})


def order_created(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "orders/created.html", {"order": order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders/history.html", {"orders": orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/detail.html", {"order": order})
