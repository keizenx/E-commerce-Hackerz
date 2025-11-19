"""
Tests d'intégration pour les vues du panier (cart_add, cart_remove, cart_update, delete_from_cart, cart_detail, cart_count)
Ces tests vérifient l'intégration entre les vues du panier, les modèles Cart/CartItem et la session.
"""
import json
import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from Hackerz_E_commerce.models import Category, Product, Cart, CartItem


def _create_test_image():
    """Créer une image de test"""
    img = Image.new('RGB', (100, 100), color='red')
    img_io = BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)
    return SimpleUploadedFile("test_image.jpg", img_io.read(), content_type="image/jpeg")


@pytest.mark.django_db
class TestCartDetailView:
    """Tests d'intégration pour la vue cart_detail"""
    
    def test_cart_detail_view_empty(self, client):
        """Test que la vue cart_detail affiche un panier vide"""
        url = reverse('shop:cart_detail')
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'cart_items' in response.context or 'total' in response.context
    
    def test_cart_detail_view_with_items(self, client):
        """Test que la vue cart_detail affiche les articles du panier"""
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
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        client.login(username='testuser', password='testpass')
        
        # Ajouter un produit au panier
        client.post(
            reverse("shop:cart_add", args=[product.id]),
            data=json.dumps({"quantity": 2}),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        
        url = reverse('shop:cart_detail')
        response = client.get(url)
        
        assert response.status_code == 200


@pytest.mark.django_db
class TestCartCountView:
    """Tests d'intégration pour la vue cart_count"""
    
    def test_cart_count_empty(self, client):
        """Test que cart_count retourne 0 pour un panier vide"""
        url = reverse('shop:cart_count')
        response = client.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert data['count'] == 0
    
    def test_cart_count_with_items(self, client):
        """Test que cart_count retourne le bon nombre d'articles"""
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
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        client.login(username='testuser', password='testpass')
        
        # Ajouter des produits au panier
        client.post(
            reverse("shop:cart_add", args=[product.id]),
            data=json.dumps({"quantity": 3}),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        
        url = reverse('shop:cart_count')
        response = client.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert data['count'] == 3


@pytest.mark.django_db
class TestCartUpdateView:
    """Tests d'intégration pour la vue cart_update"""
    
    def test_cart_update_increases_quantity(self, client):
        """Test que cart_update augmente la quantité"""
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
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        client.login(username='testuser', password='testpass')
        
        # Ajouter un produit
        client.post(
            reverse("shop:cart_add", args=[product.id]),
            data=json.dumps({"quantity": 1}),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        
        # Mettre à jour la quantité (POST standard, pas JSON)
        response = client.post(
            reverse("shop:cart_update", args=[product.id]),
            data={"quantity": 3},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        
        assert response.status_code == 200
        cart_item = CartItem.objects.get(product=product)
        assert cart_item.quantity == 3
    
    def test_cart_update_exceeds_stock(self, client):
        """Test que cart_update refuse une quantité supérieure au stock"""
        category = Category.objects.create(name="Electronics", slug="electronics")
        image = _create_test_image()
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            category=category,
            regular_price=Decimal("99.99"),
            price=Decimal("79.99"),
            stock=2,
            available=True,
            image=image
        )
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        client.login(username='testuser', password='testpass')
        
        # Ajouter un produit
        client.post(
            reverse("shop:cart_add", args=[product.id]),
            data=json.dumps({"quantity": 1}),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        
        initial_quantity = CartItem.objects.get(product=product).quantity
        
        # Essayer de mettre à jour avec une quantité trop élevée (POST standard)
        response = client.post(
            reverse("shop:cart_update", args=[product.id]),
            data={"quantity": 5},  # Plus que le stock (2)
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        
        # La vue ne retourne pas d'erreur, elle ne met simplement pas à jour
        # Vérifier que la quantité n'a pas changé
        cart_item = CartItem.objects.get(product=product)
        assert cart_item.quantity == initial_quantity  # Reste à 1, pas mis à jour à 5


@pytest.mark.django_db
class TestDeleteFromCartView:
    """Tests d'intégration pour la vue delete_from_cart"""
    
    def test_delete_from_cart(self, client):
        """Test que delete_from_cart supprime un article du panier"""
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
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        client.login(username='testuser', password='testpass')
        
        # Ajouter un produit
        client.post(
            reverse("shop:cart_add", args=[product.id]),
            data=json.dumps({"quantity": 2}),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        
        assert CartItem.objects.filter(product=product).exists()
        
        # Supprimer le produit
        response = client.post(
            reverse("shop:delete_from_cart", args=[product.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        
        assert response.status_code in [200, 302]
        assert not CartItem.objects.filter(product=product).exists()

