from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import SignUpForm


class UnifiedLoginView(auth_views.LoginView):
    template_name = "accounts/login.html"

    def get_success_url(self):
        url = self.get_redirect_url()
        if url:
            return url
        user = self.request.user
        if user.is_authenticated and (user.is_staff or user.is_superuser):
            return "/admin/"
        return reverse("store:product_list")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("store:product_list")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})
