from django.test import TestCase
from django.urls import reverse
from store.models import Category, Product


class CartFlowTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Perfume", slug="perfume")
        self.product = Product.objects.create(
            category=self.category,
            name="Lunelle Fleur",
            slug="lunelle-fleur",
            price=350,
            stock=10,
            is_active=True
        )

    def test_add_to_cart_stays_on_page(self):
        # Adding to cart should NOT redirect to checkout or cart page
        response = self.client.post(reverse("cart:cart_add", args=[self.product.id]), {
            "quantity": 2
        }, HTTP_REFERER=self.product.get_absolute_url())
        self.assertRedirects(response, self.product.get_absolute_url())
        self.assertEqual(len(self.client.session["cart"]), 1)

    def test_add_to_cart_ajax(self):
        response = self.client.post(
            reverse("cart:cart_add", args=[self.product.id]),
            {"quantity": 1},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["cart_count"], 1)
        self.assertIn("added to cart", data["message"].lower())
