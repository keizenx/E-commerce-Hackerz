import json
from types import SimpleNamespace
from uuid import uuid4
from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from Hackerz_E_commerce.models import Product, Category
from Hackerz.models import Vendor


pytestmark = pytest.mark.django_db


def _gif_image(name: str = "test.gif") -> SimpleUploadedFile:
    """Create a tiny valid GIF image for upload tests."""
    gif_bytes = (
        b"GIF89a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00"
        b"\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00"
        b"\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02L\x01\x00;"
    )
    return SimpleUploadedFile(name, gif_bytes, content_type="image/gif")


def _unique_name(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:6]}"


def test_authorised_vendor_can_create_product(client, vendor_user, category):
    client.force_login(vendor_user)
    url = reverse("shop:add_product")
    name = _unique_name("Vendor Product")
    payload = {
        "name": name,
        "category": category.id,
        "price": "149.99",
        "regular_price": "179.99",
        "stock": "10",
        "description": "Produit ajouté par un vendeur approuvé.",
        "available": "on",
        "featured": "on",
        "image": _gif_image("vendor-product.gif"),
    }

    response = client.post(
        url,
        data=payload,
        HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert Product.objects.filter(name=name, vendor=vendor_user.profile.vendor).exists()


def test_vendor_dashboard_lists_their_products(client, vendor_user, category):
    vendor = vendor_user.profile.vendor
    product = Product.objects.create(
        vendor=vendor,
        category=category,
        name=_unique_name("Dashboard Product"),
        slug=_unique_name("dashboard-product"),
        description="Produit du vendeur visible dans le tableau de bord.",
        regular_price="120.00",
        price="99.99",
        stock=5,
        available=True,
    )

    client.force_login(vendor_user)
    response = client.get(reverse("shop:vendor_products"))

    assert response.status_code == 200
    assert product in response.context["products"]


def test_visitor_registration_creates_inactive_account(client):
    username = _unique_name("visitor")
    response = client.post(
        reverse("register"),
        data={
            "username": username,
            "first_name": "Visi",
            "last_name": "Tor",
            "email": f"{username}@example.com",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
        },
    )

    assert response.status_code == 302
    created_user = User.objects.get(username=username)
    assert created_user.is_active is False


def test_authenticated_customer_can_add_products_to_cart(client, category):
    customer = User.objects.create_user(
        username=_unique_name("customer"),
        email="customer@example.com",
        password="CustomerPass123!",
    )
    product = Product.objects.create(
        category=category,
        name=_unique_name("Public Product"),
        slug=_unique_name("public-product"),
        description="Produit public disponible pour les clients.",
        regular_price="59.99",
        price="39.99",
        stock=12,
        available=True,
    )

    client.force_login(customer)
    response = client.post(
        reverse("shop:cart_add", args=[product.id]),
        data=json.dumps({"quantity": 2}),
        content_type="application/json",
        HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["total_items"] == 2


def test_guest_is_redirected_to_login_before_checkout(client):
    response = client.get(reverse("shop:checkout"))
    assert response.status_code == 302
    assert reverse("login") in response.url


def test_admin_can_approve_vendor(client, admin_user, vendor_user):
    vendor = vendor_user.profile.vendor
    vendor.is_approved = False
    vendor.save()

    client.force_login(admin_user)

    class DummyEmail:
        def __init__(self, *args, **kwargs):
            pass

        def attach_alternative(self, *args, **kwargs):
            return None

        def send(self, fail_silently=False):
            return 1

    with patch("django.core.mail.EmailMultiAlternatives", return_value=DummyEmail()), patch(
        "django.contrib.sites.shortcuts.get_current_site", return_value=SimpleNamespace(domain="testserver")
    ):
        response = client.get(f"/admin/Hackerz/vendor/{vendor.id}/approve/")

    assert response.status_code == 302
    vendor.refresh_from_db()
    assert vendor.is_approved is True


@pytest.mark.django_db
def test_registration_rejects_duplicate_credentials(client, create_user):
    existing = create_user(username="dupuser", email="dup@example.com")

    response = client.post(
        reverse("register"),
        {
            "username": existing.username,
            "first_name": "Dup",
            "last_name": "User",
            "email": existing.email,
            "password1": "DupPass123!",
            "password2": "DupPass123!",
        },
    )

    assert response.status_code == 200
    assert User.objects.filter(username="dupuser").count() == 1
    body = response.content
    assert (b"Un utilisateur avec ce nom existe" in body) or (b"Cet email est deja" in body) or (b"Cet email est d" in body)


def test_non_vendor_cannot_access_vendor_dashboard(client, create_user):
    user = create_user(username=_unique_name("basic"), email="basic@example.com")
    client.force_login(user)

    response = client.get(reverse("shop:vendor_products"))

    assert response.status_code == 302
    assert reverse("profile") in response.url


def test_unapproved_vendor_cannot_add_product(client, create_user, category):
    user = create_user(username=_unique_name("pending"), email="pending@example.com")
    profile = user.profile
    profile.is_vendor = True
    profile.save()
    Vendor.objects.create(
        profile=profile,
        shop_name="Pending Shop",
        description="En attente d'approbation",
        is_approved=False,
    )

    client.force_login(user)

    response = client.post(
        reverse("shop:add_product"),
        data={
            "name": "Produit refusé",
            "category": category.id,
            "price": "19.99",
            "regular_price": "29.99",
            "stock": "5",
            "description": "Produit d'un vendeur non approuvé.",
            "available": "on",
            "featured": "",
            "image": _gif_image("pending-product.gif"),
        },
        HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )

    assert response.status_code == 302
    assert reverse("profile") in response.url
    assert not Product.objects.filter(name="Produit refusé").exists()

