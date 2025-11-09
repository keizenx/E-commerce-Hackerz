import os
import shutil
import tempfile
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase, override_settings

from Hackerz_E_commerce import utils
from Hackerz_E_commerce.models import Category, Order, OrderItem, Product


class InvoiceUtilsTests(TestCase):
    def setUp(self):
        self.temp_media = tempfile.mkdtemp()
        self.override = override_settings(MEDIA_ROOT=self.temp_media)
        self.override.enable()

        category = Category.objects.create(name="Printing")
        self.product = Product.objects.create(
            category=category,
            name="3D Printer",
            regular_price=Decimal("999.99"),
            price=Decimal("899.99"),
            stock=5,
            available=True,
        )
        self.user = User.objects.create_user(username="alice", password="secret123")
        self.order = Order.objects.create(
            user=self.user,
            first_name="Alice",
            last_name="Doe",
            email="alice@example.com",
            address="1 Infinite Loop",
            postal_code="75000",
            city="Paris",
            paid=True,
        )
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=self.product.price,
            quantity=1,
        )

    def tearDown(self):
        self.override.disable()
        shutil.rmtree(self.temp_media, ignore_errors=True)

    @patch("Hackerz_E_commerce.utils.pisa.pisaDocument")
    def test_save_invoice_pdf_creates_file(self, mock_pisa):
        def fake_pisa_document(_, result_buffer, **kwargs):
            result_buffer.write(b"PDF-CONTENT")
            return SimpleNamespace(err=False)

        mock_pisa.side_effect = fake_pisa_document

        relative_path = utils.save_invoice_pdf(self.order)

        expected_filename = f"facture_{self.order.id}.pdf"
        self.assertIsNotNone(relative_path)
        self.assertTrue(relative_path.endswith(expected_filename))

        saved_path = os.path.join(self.temp_media, relative_path)
        self.assertTrue(os.path.exists(saved_path))

    @patch("Hackerz_E_commerce.utils.pisa.pisaDocument")
    def test_generate_invoice_pdf_returns_response(self, mock_pisa):
        def fake_pisa_document(_, result_buffer, **kwargs):
            result_buffer.write(b"PDF-CONTENT")
            return SimpleNamespace(err=False)

        mock_pisa.side_effect = fake_pisa_document

        response = utils.generate_invoice_pdf(self.order)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertIn(f'filename="facture_{self.order.id}.pdf"', response["Content-Disposition"])
        self.assertEqual(response.content, b"PDF-CONTENT")