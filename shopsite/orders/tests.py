from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from cart.cart import Cart
from orders.models import Order
from store.models import Category, Product


class OrderModalCheckoutTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Perfume", slug="perfume")
        self.product = Product.objects.create(
            category=self.category,
            name="Lunelle Rose",
            slug="lunelle-rose",
            price=450,
            stock=15,
            is_active=True
        )
        self.user = User.objects.create_user(username="testclient", password="password123")

    def _add_item_to_cart(self):
        session = self.client.session
        session["cart"] = {str(self.product.id): {"quantity": 2, "price": "450.00"}}
        session.save()

    def test_cash_checkout_order(self):
        self._add_item_to_cart()
        response = self.client.post(reverse("orders:order_create"), {
            "full_name": "Maria Clara",
            "contact": "09123456789 / @mariaclara_ig",
            "note": "Gift wrap please ♡",
            "payment_method": "cash",
        })
        order = Order.objects.latest("id")
        self.assertEqual(order.full_name, "Maria Clara")
        self.assertEqual(order.contact, "09123456789 / @mariaclara_ig")
        self.assertEqual(order.note, "Gift wrap please ♡")
        self.assertEqual(order.payment_method, "cash")
        self.assertEqual(order.get_total_cost(), 900)
        self.assertRedirects(response, reverse("orders:order_created", args=[order.id]))

    def test_ewallet_checkout_order(self):
        self._add_item_to_cart()
        response = self.client.post(reverse("orders:order_create"), {
            "full_name": "Juan Dela Cruz",
            "contact": "GCash: 09987654321",
            "note": "Leaving outside gate",
            "payment_method": "ewallet",
        })
        order = Order.objects.latest("id")
        self.assertEqual(order.payment_method, "ewallet")
        self.assertEqual(order.contact, "GCash: 09987654321")
        self.assertRedirects(response, reverse("orders:order_created", args=[order.id]))

    def test_ajax_checkout_returns_json_redirect(self):
        self._add_item_to_cart()
        response = self.client.post(
            reverse("orders:order_create"),
            {
                "full_name": "Anna Santos",
                "contact": "@annasantos_ig",
                "note": "Mint shade",
                "payment_method": "ewallet",
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("created", data["redirect_url"])
