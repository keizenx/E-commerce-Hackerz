"""
Tests d'intégration pour la vue buy_now
Ces tests vérifient l'intégration entre la vue buy_now, le panier et le checkout.
"""
import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from Hackerz_E_commerce.models import Category, Product, Cart, CartItem
from Hackerz.models import Profile, Vendor


def _create_test_image():
    """Créer une image de test"""
    img = Image.new('RGB', (100, 100), color='red')
    img_io = BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)
    return SimpleUploadedFile("test_image.jpg", img_io.read(), content_type="image/jpeg")


@pytest.mark.django_db
class TestBuyNowView:
    """Tests d'intégration pour la vue buy_now"""
    
    def test_buy_now_requires_login(self, client):
        """Test que buy_now exige une authentification"""
        category = Category.objects.create(name="Electronics", slug="electronics")
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            category=category,
            regular_price=Decimal("99.99"),
            price=Decimal("79.99"),
            stock=10,
            available=True
        )
        
        response = client.post(reverse('shop:buy_now', args=[product.id]), {
            'quantity': 1
        })
        
        assert response.status_code == 302
        assert 'login' in response.url.lower()
    
    def test_buy_now_creates_cart_and_redirects(self, client):
        """Test que buy_now crée un panier et redirige vers checkout"""
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        # Profile créé automatiquement via signal
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
        client.login(username='testuser', password='testpass')
        
        response = client.post(reverse('shop:buy_now', args=[product.id]), {
            'quantity': 2
        })
        
        assert response.status_code == 302
        assert 'checkout' in response.url
        # Vérifier que le produit a été ajouté au panier
        cart = Cart.objects.get(cart_id=client.session.get('cart_id'))
        assert CartItem.objects.filter(cart=cart, product=product, quantity=2).exists()
    
    def test_buy_now_clears_existing_cart(self, client):
        """Test que buy_now vide le panier existant avant d'ajouter le nouveau produit"""
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        # Profile créé automatiquement via signal
        category = Category.objects.create(name="Electronics", slug="electronics")
        image = _create_test_image()
        product1 = Product.objects.create(
            name="Product 1",
            slug="product-1",
            category=category,
            regular_price=Decimal("99.99"),
            price=Decimal("79.99"),
            stock=10,
            available=True,
            image=image
        )
        product2 = Product.objects.create(
            name="Product 2",
            slug="product-2",
            category=category,
            regular_price=Decimal("149.99"),
            price=Decimal("129.99"),
            stock=5,
            available=True,
            image=image
        )
        client.login(username='testuser', password='testpass')
        
        # Créer un panier en utilisant cart_add pour initialiser correctement la session
        # Cela garantit que le cart_id est correctement stocké dans la session
        import json
        client.post(
            reverse("shop:cart_add", args=[product1.id]),
            data=json.dumps({"quantity": 1}),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        
        # Récupérer le cart_id de la session
        cart_id = client.session.get('cart_id')
        assert cart_id is not None, "cart_id doit être dans la session après cart_add"
        cart = Cart.objects.get(cart_id=cart_id)
        
        # Vérifier que product1 est dans le panier
        assert CartItem.objects.filter(cart=cart, product=product1).exists()
        
        # Utiliser buy_now pour product2 (doit vider le panier et ajouter product2)
        response = client.post(reverse('shop:buy_now', args=[product2.id]), {
            'quantity': 1
        })
        
        assert response.status_code == 302
        # Vérifier que product1 n'est plus dans le panier
        cart.refresh_from_db()
        assert not CartItem.objects.filter(cart=cart, product=product1).exists()
        # Vérifier que product2 est dans le panier
        assert CartItem.objects.filter(cart=cart, product=product2).exists()
    
    def test_buy_now_vendor_cannot_buy_own_product(self, client):
        """Test qu'un vendeur ne peut pas acheter ses propres produits"""
        user = User.objects.create_user(username='vendor', email='vendor@example.com', password='testpass')
        profile = user.profile  # Profile créé automatiquement via signal
        profile.is_vendor = True
        profile.save()
        vendor = Vendor.objects.create(profile=profile, shop_name="Vendor Shop", is_approved=True)
        category = Category.objects.create(name="Electronics", slug="electronics")
        image = _create_test_image()
        product = Product.objects.create(
            name="Vendor Product",
            slug="vendor-product",
            category=category,
            vendor=vendor,
            regular_price=Decimal("99.99"),
            price=Decimal("79.99"),
            stock=10,
            available=True,
            image=image
        )
        client.login(username='vendor', password='testpass')
        
        response = client.post(reverse('shop:buy_now', args=[product.id]), {
            'quantity': 1
        })
        
        assert response.status_code == 302
        assert 'product' in response.url.lower()
    
    def test_buy_now_invalid_quantity(self, client):
        """Test que buy_now rejette une quantité invalide"""
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        # Profile créé automatiquement via signal
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
        client.login(username='testuser', password='testpass')
        
        response = client.post(reverse('shop:buy_now', args=[product.id]), {
            'quantity': 10  # Plus que le stock disponible
        })
        
        assert response.status_code == 302
        # Le produit ne devrait pas être ajouté au panier
        cart_id = client.session.get('cart_id')
        if cart_id:
            try:
                cart = Cart.objects.get(cart_id=cart_id)
                assert not CartItem.objects.filter(cart=cart, product=product).exists()
            except Cart.DoesNotExist:
                pass

