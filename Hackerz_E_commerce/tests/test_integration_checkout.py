"""
Tests d'intégration pour les vues de checkout (checkout, process_payment, payment_success)
Ces tests vérifient l'intégration entre le checkout, le paiement et la création de commandes.
"""
import json
import pytest
from decimal import Decimal
from unittest.mock import patch
from django.contrib.auth.models import User
from django.urls import reverse
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from Hackerz_E_commerce.models import Category, Product, CartItem, Order, OrderItem
from Hackerz.models import Profile


def _create_test_image():
    """Créer une image de test"""
    img = Image.new('RGB', (100, 100), color='red')
    img_io = BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)
    return SimpleUploadedFile("test_image.jpg", img_io.read(), content_type="image/jpeg")


@pytest.mark.django_db
class TestCheckoutView:
    """Tests d'intégration pour la vue checkout"""
    
    def test_checkout_requires_login(self, client):
        """Test que checkout exige une authentification"""
        url = reverse('shop:checkout')
        response = client.get(url)
        
        assert response.status_code == 302
        assert 'login' in response.url.lower()
    
    def test_checkout_with_items(self, client):
        """Test que checkout affiche le récapitulatif avec des articles"""
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
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass',
            first_name='Test',
            last_name='User'
        )
        # Profile créé automatiquement via signal
        client.login(username='testuser', password='testpass')
        
        # Ajouter un produit au panier
        client.post(
            reverse("shop:cart_add", args=[product.id]),
            data=json.dumps({"quantity": 2}),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        
        url = reverse('shop:checkout')
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'total' in response.context or 'cart_items' in response.context
    
    def test_checkout_empty_cart(self, client):
        """Test que checkout redirige si le panier est vide"""
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        # Profile créé automatiquement via signal
        client.login(username='testuser', password='testpass')
        
        url = reverse('shop:checkout')
        response = client.get(url)
        
        # Peut rediriger ou afficher un message d'erreur
        assert response.status_code in [200, 302]


@pytest.mark.django_db
class TestProcessPaymentView:
    """Tests d'intégration pour la vue process_payment"""
    
    @patch('Hackerz_E_commerce.views.save_invoice_pdf')
    def test_process_payment_creates_order(self, mock_save_invoice, client):
        """Test que process_payment crée une commande"""
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
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass',
            first_name='Test',
            last_name='User'
        )
        # Profile créé automatiquement via signal
        client.login(username='testuser', password='testpass')
        
        # Ajouter un produit au panier
        client.post(
            reverse("shop:cart_add", args=[product.id]),
            data=json.dumps({"quantity": 2}),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        
        mock_save_invoice.return_value = "invoices/test.pdf"
        
        # Traiter le paiement
        response = client.post(reverse('shop:process_payment'), {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'address': '123 Test St',
            'city': 'Test City',
            'postal_code': '12345',
            'country': 'france'
        })
        
        assert response.status_code in [200, 302]
        assert Order.objects.filter(user=user).exists()
        order = Order.objects.get(user=user)
        assert order.paid is True
        assert OrderItem.objects.filter(order=order, product=product).exists()
    
    def test_process_payment_updates_stock(self, client):
        """Test que process_payment met à jour le stock"""
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
        initial_stock = product.stock
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass',
            first_name='Test',
            last_name='User'
        )
        # Profile créé automatiquement via signal
        client.login(username='testuser', password='testpass')
        
        # Ajouter un produit au panier
        client.post(
            reverse("shop:cart_add", args=[product.id]),
            data=json.dumps({"quantity": 3}),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        
        with patch('Hackerz_E_commerce.views.save_invoice_pdf', return_value="invoices/test.pdf"):
            # Traiter le paiement
            client.post(reverse('shop:process_payment'), {
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'test@example.com',
                'address': '123 Test St',
                'city': 'Test City',
                'postal_code': '12345',
                'country': 'france'
            })
        
        product.refresh_from_db()
        assert product.stock == initial_stock - 3


@pytest.mark.django_db
class TestPaymentSuccessView:
    """Tests d'intégration pour la vue payment_success"""
    
    def test_payment_success_with_order(self, client):
        """Test que payment_success affiche la confirmation"""
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
        
        # Créer une commande
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
            quantity=1,
            price=product.price
        )
        
        # Simuler la session avec order_complete
        session = client.session
        session['order_complete'] = {
            'order_id': order.id,
            'total': str(order.get_total_cost()),
            'email': order.email
        }
        session.save()
        
        url = reverse('shop:payment_success')
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'order' in response.context
    
    def test_payment_success_without_order(self, client):
        """Test que payment_success redirige si pas de commande"""
        url = reverse('shop:payment_success')
        response = client.get(url)
        
        assert response.status_code == 302

