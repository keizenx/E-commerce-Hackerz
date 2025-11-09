from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from Hackerz_E_commerce.models import (
    Cart,
    CartItem,
    Category,
    Coupon,
    Order,
    OrderItem,
    Product,
    Review,
)


class CategoryModelTests(TestCase):
    def test_slug_is_automatically_generated(self):
        category = Category.objects.create(name="High Tech")

        self.assertEqual(category.slug, "high-tech")
        self.assertEqual(
            category.get_absolute_url(),
            reverse("shop:category_view", args=[category.slug]),
        )


class ProductModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Gaming")

    def test_formatted_description_enriches_markdown(self):
        product = Product.objects.create(
            category=self.category,
            name="Gaming Laptop",
            description="## Specs\n\n```\nprint('hello')\n```",
            regular_price=Decimal("1999.99"),
            price=Decimal("1499.99"),
            stock=5,
            available=True,
        )

        html = product.formatted_description()

        self.assertIn("<h2>Specs</h2>", html)
        self.assertIn("codehilite", html)
        self.assertIn(product.name, str(product))


class OrderModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="buyer", password="pass1234")
        self.category = Category.objects.create(name="Accessories")
        self.product = Product.objects.create(
            category=self.category,
            name="Gaming Mouse",
            regular_price=Decimal("79.99"),
            price=Decimal("59.99"),
            stock=10,
            available=True,
        )

    def test_order_total_cost_is_sum_of_items(self):
        order = Order.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            address="123 Street",
            postal_code="75001",
            city="Paris",
            paid=True,
        )
        OrderItem.objects.create(order=order, product=self.product, price=self.product.price, quantity=2)
        OrderItem.objects.create(
            order=order, product=self.product, price=Decimal("49.99"), quantity=1
        )

        self.assertEqual(order.get_total_cost(), Decimal("169.97"))

    def test_order_item_cost(self):
        order = Order.objects.create(
            user=self.user,
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
            address="456 Avenue",
            postal_code="69001",
            city="Lyon",
            paid=True,
        )
        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            price=self.product.price,
            quantity=3,
        )

        self.assertEqual(order_item.get_cost(), Decimal("179.97"))


class CouponModelTests(TestCase):
    def setUp(self):
        now = timezone.now()
        self.coupon = Coupon.objects.create(
            code="WELCOME10",
            discount_type="percentage",
            discount_value=Decimal("10"),
            min_purchase=Decimal("50"),
            max_uses=0,
            valid_from=now - timedelta(days=1),
            valid_to=now + timedelta(days=1),
            active=True,
        )

    def test_coupon_validity_checks(self):
        is_valid, message = self.coupon.is_valid()
        self.assertTrue(is_valid, message)

        self.coupon.active = False
        self.coupon.save()
        is_active, _ = self.coupon.is_valid()
        self.assertFalse(is_active)

    def test_coupon_date_constraints(self):
        now = timezone.now()
        coupon = Coupon.objects.create(
            code="FUTURE",
            discount_type="percentage",
            discount_value=Decimal("5"),
            min_purchase=Decimal("0"),
            max_uses=0,
            valid_from=now + timedelta(days=1),
            valid_to=now + timedelta(days=2),
            active=True,
        )
        is_valid, _ = coupon.is_valid()
        self.assertFalse(is_valid)

        coupon.valid_from = now - timedelta(days=2)
        coupon.valid_to = now - timedelta(days=1)
        coupon.save(update_fields=["valid_from", "valid_to"])
        is_valid, _ = coupon.is_valid()
        self.assertFalse(is_valid)

    def test_coupon_usage_limit(self):
        self.coupon.max_uses = 1
        self.coupon.used_count = 1
        self.coupon.save()
        is_valid, _ = self.coupon.is_valid()
        self.assertFalse(is_valid)

    def test_coupon_discount_calculations(self):
        total = Decimal("200")

        new_total, discount = self.coupon.apply_discount(total)
        self.assertEqual(discount, Decimal("20"))
        self.assertEqual(new_total, Decimal("180"))

        fixed_coupon = Coupon.objects.create(
            code="FIXED50",
            discount_type="fixed",
            discount_value=Decimal("50"),
            min_purchase=Decimal("0"),
            max_uses=0,
            valid_from=timezone.now() - timedelta(days=1),
            valid_to=timezone.now() + timedelta(days=1),
            active=True,
        )

        new_total, discount = fixed_coupon.apply_discount(Decimal("30"))
        self.assertEqual(discount, Decimal("30"))
        self.assertEqual(new_total, Decimal("0"))


class CartModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Audio")
        self.product = Product.objects.create(
            category=self.category,
            name="Headphones",
            regular_price=Decimal("199.99"),
            price=Decimal("149.99"),
            stock=15,
            available=True,
        )
        self.cart = Cart.objects.create(cart_id="session123")

    def test_cart_item_subtotal(self):
        cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2,
        )

        self.assertEqual(cart_item.sub_total(), Decimal("299.98"))
        self.assertEqual(str(cart_item), "Headphones")


class ReviewModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reviewer", password="secret123")
        self.category = Category.objects.create(name="Books")
        self.product = Product.objects.create(
            category=self.category,
            name="Python 101",
            regular_price=Decimal("39.99"),
            price=Decimal("29.99"),
            stock=20,
            available=True,
        )

    def test_review_string_representation(self):
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            title="Great book",
            comment="Very informative",
        )

        self.assertEqual(str(review), f"Avis de {self.user.username} sur {self.product.name}")

