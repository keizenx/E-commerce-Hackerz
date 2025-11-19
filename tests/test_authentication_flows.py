import json
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from django.test import override_settings
from django.urls import reverse

from Hackerz.models import NewsletterSubscriber


pytestmark = pytest.mark.django_db


@override_settings(DEFAULT_FROM_EMAIL="no-reply@example.com")
def test_register_ajax_success_creates_inactive_user(client):
    payload = {
        "username": "newuser",
        "first_name": "New",
        "last_name": "User",
        "email": "newuser@example.com",
        "password1": "StrongPass123!",
        "password2": "StrongPass123!",
    }

    with patch("Hackerz.views.get_current_site", return_value=SimpleNamespace(domain="testserver")), patch(
        "Hackerz.views.send_mail"
    ) as mocked_send_mail, patch("Hackerz.views.render_to_string", return_value="<p>Email</p>"):
        response = client.post(
            reverse("register"),
            data=payload,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["redirect_url"] == reverse("registration_success")

    user = User.objects.get(username="newuser")
    assert user.is_active is False
    mocked_send_mail.assert_called_once()


def test_register_ajax_duplicates_return_error(client, create_user):
    existing = create_user(username="duplicate", email="dup@example.com")

    response = client.post(
        reverse("register"),
        data={
            "username": existing.username,
            "first_name": "Dup",
            "last_name": "User",
            "email": existing.email,
            "password1": "DupPass123!",
            "password2": "DupPass123!",
        },
        HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["success"] is False
    assert payload["message"]


def test_login_ajax_success_returns_json(client, create_user):
    user = create_user(username="authuser", email="auth@example.com", password="AuthPass123!")

    response = client.post(
        reverse("login"),
        data={"username": user.email, "password": "AuthPass123!"},
        HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["redirect_url"] == reverse("home")


def test_login_ajax_invalid_credentials_returns_error(client):
    response = client.post(
        reverse("login"),
        data={"username": "unknown@example.com", "password": "wrong"},
        HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["success"] is False
    assert "email" in payload["message"].lower()


def test_logout_redirects_to_home(client, create_user):
    user = create_user(username="logoutuser", email="logout@example.com")
    client.force_login(user)

    response = client.get(reverse("logout"))

    assert response.status_code == 302
    assert response.url == reverse("home")


def test_newsletter_signup_ajax_creates_subscriber(client):
    response = client.post(
        reverse("newsletter_signup"),
        data={"email": "subscriber@example.com"},
        HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert NewsletterSubscriber.objects.filter(email="subscriber@example.com").exists()


def test_newsletter_signup_ajax_rejects_missing_email(client):
    response = client.post(
        reverse("newsletter_signup"),
        data={"email": ""},
        HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["success"] is False
    assert "adresse email valide" in payload["message"].lower()

