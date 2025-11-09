import json
import tempfile
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from Hackerz_E_commerce.models import CartItem, Category, Order, OrderItem, Product


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    MEDIA_ROOT=tempfile.gettempdir(),
)
class FunctionalCheckoutTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Smartphones")
        self.product = Product.objects.create(
            category=self.category,
            name="Smartphone Pro",
            regular_price=Decimal("1099.99"),
            price=Decimal("999.99"),
            stock=5,
            available=True,
        )
        self.user = User.objects.create_user(
            username="customer",
            password="secret123",
            email="customer@example.com",
            first_name="Jane",
            last_name="Doe",
        )

    def _add_product_to_cart(self, quantity=1):
        self.client.login(username="customer", password="secret123")
        response = self.client.post(
            reverse("shop:cart_add", args=[self.product.id]),
            data=json.dumps({"quantity": quantity}),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItem.objects.count(), 1)

    @patch("Hackerz_E_commerce.views.save_invoice_pdf", return_value="invoices/facture_test.pdf")
    def test_customer_can_complete_checkout_flow(self, mock_save_invoice):
        self._add_product_to_cart(quantity=2)

        payment_response = self.client.post(
            reverse("shop:process_payment"),
            data={
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "jane.doe@example.com",
                "address": "221B Baker Street",
                "city": "London",
                "postal_code": "NW1",
                "country": "uk",
            },
        )

        self.assertEqual(payment_response.status_code, 302)
        self.assertEqual(payment_response["Location"], reverse("shop:payment_success"))

        session = self.client.session
        self.assertIn("order_complete", session)

        order = Order.objects.get()
        self.assertEqual(order.email, "jane.doe@example.com")
        self.assertEqual(order.status, "processing")
        self.assertTrue(order.paid)

        order_item = OrderItem.objects.get(order=order)
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.price, self.product.price)

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)

        mock_save_invoice.assert_called_once_with(order)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(str(order.id), mail.outbox[0].subject)
        self.assertIn("jane.doe@example.com", mail.outbox[0].to)

        success_response = self.client.get(reverse("shop:payment_success"))
        self.assertEqual(success_response.status_code, 200)
        self.assertNotIn("order_complete", self.client.session)

