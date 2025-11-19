from decimal import Decimal
import io
import uuid
from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone
from PIL import Image

from Hackerz.models import NewsletterSubscriber, Wishlist
from Hackerz_E_commerce.models import Product, Order, OrderItem
from Hackerz_blog.models import Category as BlogCategory, Post, PostView, Tag


pytestmark = pytest.mark.django_db


def _dummy_image_file(name: str = "image.png") -> SimpleUploadedFile:
    image = Image.new("RGB", (10, 10), color="white")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return SimpleUploadedFile(name, buffer.read(), content_type="image/png")


def _create_featured_product(category, name="Featured Product"):
    slug_base = name.lower().replace(" ", "-")
    slug_value = f"{slug_base}-{uuid.uuid4().hex[:8]}"
    return Product.objects.create(
        category=category,
        name=name,
        slug=slug_value,
        regular_price=Decimal("99.99"),
        price=Decimal("79.99"),
        stock=5,
        available=True,
        featured=True,
        image=_dummy_image_file(f"{slug_value}.png"),
    )


def _create_blog_post(author):
    blog_category = BlogCategory.objects.create(name="Tech", slug=f"tech-{uuid.uuid4().hex[:8]}")
    tag = Tag.objects.create(name="Innovation", slug=f"innovation-{uuid.uuid4().hex[:8]}")
    slug_value = f"dernieres-nouveautes-{uuid.uuid4().hex[:8]}"
    post = Post.objects.create(
        title="Dernières nouveautés",
        slug=slug_value,
        author=author,
        content="## Nouveautés\nContenu de test.",
        category=blog_category,
        status="published",
        image=_dummy_image_file(f"{slug_value}.png"),
    )
    post.tags.add(tag)
    return post


def test_home_view_lists_products_and_posts(client, create_category, settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    settings.MEDIA_URL = "/media/"
    shop_category = create_category()
    featured_product = _create_featured_product(shop_category)
    author = User.objects.create_user(username="author", email="author@example.com", password="AuthorPass123!")
    blog_post = _create_blog_post(author)

    response = client.get(reverse("home"))

    assert response.status_code == 200
    assert featured_product in response.context["featured_products"]
    assert blog_post in response.context["recent_posts"]


@override_settings(DEFAULT_FROM_EMAIL="no-reply@example.com")
def test_contact_view_sends_email_and_redirects(client):
    with patch("Hackerz.views.send_mail", return_value=1) as mocked_send_mail:
        response = client.post(
            reverse("contact"),
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "subject": "Demande d'information",
                "message": "Bonjour, j'ai une question sur vos produits.",
            },
        )

    assert response.status_code == 302
    assert response.url == reverse("contact")
    mocked_send_mail.assert_called_once()


def test_contact_view_get_returns_form(client):
    response = client.get(reverse("contact"))
    assert response.status_code == 200
    assert "form" in response.context


def test_profile_view_collects_recent_activities(client, create_category, create_user, settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    settings.MEDIA_URL = "/media/"
    user = create_user(username="profileuser", email="profile@example.com", password="ProfilePass123!")
    shop_category = create_category()
    slug_value = f"profile-product-{uuid.uuid4().hex[:8]}"
    product = Product.objects.create(
        category=shop_category,
        name="Profile Product",
        slug=slug_value,
        regular_price=Decimal("49.99"),
        price=Decimal("39.99"),
        stock=3,
        available=True,
        image=_dummy_image_file(f"{slug_value}.png"),
    )
    Wishlist.objects.create(user=user)

    order = Order.objects.create(
        user=user,
        first_name="Profile",
        last_name="User",
        email="profile@example.com",
        address="1 rue du Test",
        postal_code="75000",
        city="Paris",
        paid=True,
    )
    OrderItem.objects.create(order=order, product=product, price=product.price, quantity=1)

    blog_post = _create_blog_post(user)
    PostView.objects.create(user=user, post=blog_post)

    client.force_login(user)
    response = client.get(reverse("profile"))

    assert response.status_code == 200
    recent_activities = response.context["recent_activities"]
    assert any(activity["type"] == "order" for activity in recent_activities)
    assert any(activity["type"] == "tutorial" for activity in recent_activities)


@override_settings(DEFAULT_FROM_EMAIL="no-reply@example.com")
def test_newsletter_subscribe_ajax_sends_confirmation(client):
    with patch("Hackerz.views.send_mail", return_value=1):
        response = client.post(
            reverse("newsletter_subscribe"),
            data={"email": "newsubscriber@example.com"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert NewsletterSubscriber.objects.filter(email="newsubscriber@example.com").exists()


def test_newsletter_subscribe_existing_user_returns_info(client):
    NewsletterSubscriber.objects.create(email="existing@example.com")

    response = client.post(
        reverse("newsletter_subscribe"),
        data={"email": "existing@example.com"},
        HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert "déjà inscrit" in payload["message"].lower()

