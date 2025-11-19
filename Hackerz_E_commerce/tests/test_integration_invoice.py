"""
Tests d'intégration pour la vue generate_invoice_pdf
Ces tests vérifient la génération de factures PDF.
"""
import pytest
from decimal import Decimal
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from Hackerz_E_commerce.models import Category, Product, Order, OrderItem
from Hackerz.models import Profile


def _create_test_image():
    """Créer une image de test"""
    img = Image.new('RGB', (100, 100), color='red')
    img_io = BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)
    return SimpleUploadedFile("test_image.jpg", img_io.read(), content_type="image/jpeg")


@pytest.mark.django_db
class TestGenerateInvoicePdfView:
    """Tests d'intégration pour la vue generate_invoice_pdf"""
    
    def test_generate_invoice_pdf_requires_login(self, client):
        """Test que generate_invoice_pdf exige une authentification"""
        response = client.get(reverse('shop:generate_invoice', args=[1]))
        
        assert response.status_code == 302
        assert 'login' in response.url.lower()
    
    def test_generate_invoice_pdf_requires_own_order(self, client):
        """Test qu'un utilisateur ne peut générer que ses propres factures"""
        user1 = User.objects.create_user(username='user1', email='user1@example.com', password='testpass')
        user2 = User.objects.create_user(username='user2', email='user2@example.com', password='testpass')
        # Profiles créés automatiquement via signal
        category = Category.objects.create(name="Electronics", slug="electronics")
        image = _create_test_image()
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            category=category,
            regular_price=Decimal("99.99"),
            price=Decimal("79.99"),
            stock=10,
            available=True,
            image=image
        )
        
        # Créer une commande pour user1
        order = Order.objects.create(
            user=user1,
            first_name='User',
            last_name='One',
            email='user1@example.com',
            address='123 Test St',
            city='Test City',
            postal_code='12345',
            paid=True,
            status='processing'
        )
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
            price=product.price
        )
        
        # user2 essaie d'accéder à la facture de user1
        client.login(username='user2', password='testpass')
        response = client.get(reverse('shop:generate_invoice', args=[order.id]))
        
        assert response.status_code == 404  # Commande non trouvée car pas le propriétaire
    
    @patch('Hackerz_E_commerce.views.pisa.CreatePDF')
    def test_generate_invoice_pdf_success(self, mock_pisa, client):
        """Test que generate_invoice_pdf génère un PDF avec succès"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass',
            first_name='Test',
            last_name='User'
        )
        # Profile créé automatiquement via signal
        client.login(username='testuser', password='testpass')
        
        category = Category.objects.create(name="Electronics", slug="electronics")
        image = _create_test_image()
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            category=category,
            regular_price=Decimal("99.99"),
            price=Decimal("79.99"),
            stock=10,
            available=True,
            image=image
        )
        
        order = Order.objects.create(
            user=user,
            first_name='Test',
            last_name='User',
            email='test@example.com',
            address='123 Test St',
            city='Test City',
            postal_code='12345',
            paid=True,
            status='processing'
        )
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=2,
            price=product.price
        )
        
        # Mock pisa.CreatePDF pour éviter les erreurs de génération PDF
        # pisa.CreatePDF retourne un objet avec un attribut .err
        from types import SimpleNamespace
        mock_pisa_status = SimpleNamespace(err=False)
        mock_pisa.return_value = mock_pisa_status
        
        # Le bug de Decimal a été corrigé dans views.py ligne 1320-1321
        response = client.get(reverse('shop:generate_invoice', args=[order.id]))
        
        # Vérifier que la réponse est correcte
        assert response.status_code == 200
        assert response['Content-Type'] == 'application/pdf'

