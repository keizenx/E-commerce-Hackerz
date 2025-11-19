from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
def test_vendor_request_sends_notification_email(client, create_user, tmp_path, settings):
    user = create_user(username="applicant", email="applicant@example.com")
    client.force_login(user)

    settings.MEDIA_ROOT = tmp_path

    response = client.post(
        reverse("become_vendor"),
        {
            "shop_name": "Boutique Test",
            "description": "Je souhaite vendre mes produits.",
            "phone": "+33102030405",
            "identity_document": SimpleUploadedFile(
                "identity.pdf",
                b"Fake identity document content",
                content_type="application/pdf",
            ),
        },
    )

    assert response.status_code == 302
    user.refresh_from_db()
    assert user.profile.is_vendor is True
    assert len(mail.outbox) == 1
    notification = mail.outbox[0]
    assert "Nouvelle demande de vendeur" in notification.subject
    assert "Boutique Test" in notification.body
    assert "applicant@example.com" in notification.body


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
def test_vendor_request_without_identity_document_fails(client, create_user):
    user = create_user(username="no-doc", email="no-doc@example.com")
    client.force_login(user)

    response = client.post(
        reverse("become_vendor"),
        {
            "shop_name": "Boutique incomplète",
            "description": "Je n'ai pas fourni de document.",
            "phone": "+33102030405",
        },
        HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["success"] is False
    assert user.profile.is_vendor is False
    assert "document" in payload["message"].lower() or "champ" in payload["message"].lower()
    assert len(mail.outbox) == 0
