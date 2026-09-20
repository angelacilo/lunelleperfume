from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

admin.site.login_url = "/accounts/login/"
admin.site.site_header = "Lunelle Perfume Admin"
admin.site.site_title = "Lunelle Admin"
admin.site.index_title = "Lunelle Management Dashboard"


def admin_login_redirect(request):
    next_url = request.GET.get("next", "/admin/")
    return redirect(f"/accounts/login/?next={next_url}")


urlpatterns = [
    path("admin/login/", admin_login_redirect),
    path("admin/", admin.site.urls),
    path("cart/", include("cart.urls", namespace="cart")),
    path("orders/", include("orders.urls", namespace="orders")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("", include("store.urls", namespace="store")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
