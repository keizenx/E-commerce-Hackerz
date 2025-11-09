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

