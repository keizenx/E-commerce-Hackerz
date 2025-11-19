import json
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from Hackerz_E_commerce.models import CartItem, Category, Product


class CartViewsTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Consoles")
        self.product = Product.objects.create(
            category=self.category,
            name="NextGen Console",
            regular_price=Decimal("599.99"),
            price=Decimal("499.99"),
            stock=10,
            available=True,
        )
        self.user = User.objects.create_user(username="player", email="player@example.com", password="secret123")

    def test_cart_add_requires_authentication(self):
        response = self.client.post(
            reverse("shop:cart_add", args=[self.product.id]),
            data=json.dumps({"quantity": 1}),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(CartItem.objects.count(), 0)

    def test_cart_add_creates_cart_item(self):
        self.client.login(username="player", password="secret123")

        response = self.client.post(
            reverse("shop:cart_add", args=[self.product.id]),
            data=json.dumps({"quantity": 2}),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["success"])
        self.assertEqual(payload["total_items"], 2)

        cart_item = CartItem.objects.get(product=self.product)
        self.assertEqual(cart_item.quantity, 2)

    def test_cart_remove_decrements_quantity(self):
        self.client.login(username="player", password="secret123")
        self.client.post(
            reverse("shop:cart_add", args=[self.product.id]),
            data=json.dumps({"quantity": 2}),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        response = self.client.post(
            reverse("shop:cart_remove", args=[self.product.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "success")
        self.assertEqual(payload["cart_items_count"], 1)

        cart_item = CartItem.objects.get(product=self.product)
        self.assertEqual(cart_item.quantity, 1)

    def test_checkout_requires_login(self):
        response = self.client.get(reverse("shop:checkout"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_checkout_context_contains_cart_summary(self):
        self.client.login(username="player", password="secret123")
        self.client.post(
            reverse("shop:cart_add", args=[self.product.id]),
            data=json.dumps({"quantity": 2}),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        response = self.client.get(reverse("shop:checkout"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["counter"], 2)
        self.assertEqual(response.context["total"], Decimal("999.98"))
        self.assertTrue(response.context["cart_items"])

    def test_cart_add_fails_when_product_out_of_stock(self):
        self.product.stock = 0
        self.product.available = False
        self.product.save(update_fields=["stock", "available"])

        self.client.login(username="player", password="secret123")

        response = self.client.post(
            reverse("shop:cart_add", args=[self.product.id]),
            data=json.dumps({"quantity": 1}),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 400)
        payload = response.json()
        self.assertFalse(payload["success"])
        self.assertIn("n'est plus disponible", payload["message"])
        self.assertEqual(CartItem.objects.count(), 0)

    def test_cart_add_fails_when_quantity_exceeds_stock(self):
        self.product.stock = 2
        self.product.save(update_fields=["stock"])

        self.client.login(username="player", password="secret123")

        response = self.client.post(
            reverse("shop:cart_add", args=[self.product.id]),
            data=json.dumps({"quantity": 5}),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 400)
        payload = response.json()
        self.assertFalse(payload["success"])
        self.assertIn("quantité demandée dépasse", payload["message"])
        self.assertEqual(CartItem.objects.count(), 0)

