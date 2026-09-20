from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UnifiedLoginTests(TestCase):
    def setUp(self):
        self.regular_user = User.objects.create_user(username="customer1", password="password123")
        self.staff_user = User.objects.create_user(username="admin1", password="password123", is_staff=True)

    def test_admin_login_url_redirects_to_unified_login(self):
        response = self.client.get("/admin/login/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_regular_user_login_redirects_to_store(self):
        response = self.client.post(reverse("accounts:login"), {
            "username": "customer1",
            "password": "password123"
        })
        self.assertRedirects(response, reverse("store:product_list"))

    def test_staff_user_login_redirects_to_admin(self):
        response = self.client.post(reverse("accounts:login"), {
            "username": "admin1",
            "password": "password123"
        })
        self.assertRedirects(response, "/admin/")

    def test_staff_user_login_with_next_param(self):
        response = self.client.post(f"{reverse('accounts:login')}?next=/cart/", {
            "username": "admin1",
            "password": "password123"
        })
        self.assertRedirects(response, "/cart/")

    def test_navbar_shows_admin_panel_for_staff(self):
        self.client.login(username="admin1", password="password123")
        response = self.client.get(reverse("store:product_list"))
        self.assertContains(response, "Admin Panel")
        self.assertContains(response, "Lunelle")

    def test_navbar_does_not_show_admin_panel_for_customer(self):
        self.client.login(username="customer1", password="password123")
        response = self.client.get(reverse("store:product_list"))
        self.assertNotContains(response, "Admin Panel")
        self.assertContains(response, "Lunelle")
